import logging
import re
import time
from typing import List, Dict, Optional

import appdirs
import json
import os

from js2py import eval_js
from requests import get

from .models import RequestParams

file_name = "requests_params.json"
meta_name = "meta.json"
days_to_reload = 7

logger = logging.getLogger(__name__)

WebData = Dict[str, dict]
ParamsData = Dict[str, RequestParams]


class RequestsParams:
    pattern = r'params:\s*\{(?:[^{}]|{(?:[^{}]|{[^{}]*})*})*\}'

    def __init__(self, script_srcs: List[str], webpack_url: str):
        self.script_srcs = script_srcs
        self.webpack_url = webpack_url
        self._app_dir = appdirs.user_data_dir("poe_agent_py", False)
        self._file_path = os.path.join(self._app_dir, file_name)

    def __call__(self, *args, **kwargs):
        return self.load()

    def _load_from_file(self) -> WebData:
        if os.path.exists(self._file_path):
            with open(self._file_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse json file {self._file_path}")
        else:
            logger.warning(f"File {self._file_path} not found")

        return {}

    @staticmethod
    def _load_src_script(src: str) -> str:
        resp = get(src)
        if resp.status_code != 200:
            logger.warning(f"Failed to load script {src}, status code: {resp.status_code}")

        return resp.text

    def _save_to_file(self, data: WebData):
        logger.info(f"Saving data to file {self._file_path}")
        if not os.path.exists(self._app_dir):
            try:
                os.makedirs(self._app_dir)
            except OSError:
                logger.error(f"Failed to create directory {self._app_dir}")
                return

        with open(self._file_path, "w", encoding="utf-8") as f:
            try:
                json.dump(data, f, indent=4)
            except json.JSONDecodeError:
                logger.error(f"Failed to dump json file {self._file_path}")

    def _get_chunks_srcs_js_from_wp(self, chunks_ints: list[int]) -> list[str]:
        """ get static js scripts src chunks from webpack """
        pattern = r'function\(e\)\s*\{((?!function).)*\.js"\}'

        if not self.webpack_url:
            raise RuntimeError("Failed to find webpack script in js scripts")

        chunks_js_urls = []
        wp = self._load_src_script(self.webpack_url)
        chunk_func = re.search(pattern, wp).group(0)

        if not chunk_func:
            raise RuntimeError("Failed to parse chunk function from webpack")

        chunk_script = "const chF=" + chunk_func + ";"
        for chunk in chunks_ints:
            result = eval_js(chunk_script + f"chF({chunk})")
            if "undefined" in result:
                logger.warning(f"Failed to get chunk {chunk} from webpack, result: {result}")
                continue
            chunks_js_urls.append(result)

        return chunks_js_urls

    @staticmethod
    def _get_base_url(src: str) -> str:
        return src.split("static/")[0]

    @staticmethod
    def _get_chunks_numbers(script_text: str):
        """ checks if the script contains available bots chunk number and adds it to the chunk numbers list """
        patterns = [
            r"let importSelectorModal=\(\)=>Promise\.all\(\[[^\]]*\]\)\.then",
            r"let importConfirmationModal=\(\)=>((?!function|let|const).)*\)\;"
        ]
        chunks_ints = []
        for pattern in patterns:
            if match := re.search(pattern, script_text):
                result = match.group(0)
                chunks_ints += [int(i) for i in re.findall(r'\d+', result)]
        return chunks_ints

    def _parse_requests_params(self, script: str, params: WebData):
        matches = re.findall(self.pattern, script, re.DOTALL)
        for match in matches:
            data = f'{match.replace("params:", "params=")}' + '; params'  # old: function name(params){return params}(params)
            try:
                dict_ = eval(str(eval_js(data)))
                params.update({dict_["name"]: dict_})
            except Exception as e:
                logger.error(f"Failed to parse requests params data from POE API: {e}, data: `{data}`")
                raise RuntimeError(f"Failed to parse requests params data from POE API: {e}")

    def _load_from_web(self) -> WebData:
        logger.info("Initializing source scripts...")
        if not self.script_srcs:
            raise RuntimeError("script_srcs is empty")

        chunks_ints = []
        result = {}
        for src in self.script_srcs:
            script = self._load_src_script(src)

            chunks_ints += self._get_chunks_numbers(script)
            chunks_ints = list(set(chunks_ints))
            self._parse_requests_params(script, result)

        logger.info("Getting additional scripts from webpack...")
        additional_scripts_srcs = self._get_chunks_srcs_js_from_wp(chunks_ints)
        base_url = self._get_base_url(self.script_srcs[0])
        for script in additional_scripts_srcs:
            script_text = self._load_src_script(base_url + script)
            self._parse_requests_params(script_text, result)

        logger.info("Source scripts initialized")
        return result

    def _save_meta(self) -> None:
        logger.info("Saving meta...")
        meta_path = os.path.join(self._app_dir, meta_name)
        with open(meta_path, "w", encoding="utf-8") as f:
            try:
                json.dump({"last_update": int(time.time())}, f, indent=4)
            except json.JSONDecodeError:
                logger.error(f"Failed to dump json file {meta_path}")

    def _load_meta(self) -> dict:
        logger.info("Loading meta...")
        meta_path = os.path.join(self._app_dir, meta_name)
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse json file {meta_path}")
        else:
            logger.warning(f"File {meta_path} not found")

        return {}

    def _load_from_web_and_save(self):
        result = self._load_from_web()
        self._save_to_file(result)
        self._save_meta()
        return result

    def reload_if_needed(self) -> Optional[ParamsData]:
        logger.info("Checking if reload is needed...")
        if not (meta := self._load_meta()):
            logger.info("Meta not found, reloading...")
            return self.reload()
        if (time.time() - meta["last_update"]) / 86400 > days_to_reload:
            logger.info("Reload is needed, reloading...")
            return self.reload()
        logger.info("Reload is not needed")

    def load(self) -> ParamsData:
        logger.info("Loading requests params data...")
        if not (result := self._load_from_file()):
            logger.info("Result not found in file, loading from web...")
            result = self._load_from_web_and_save()

        return {key: RequestParams(**value) for key, value in result.items()}

    def reload(self, script_srcs: List[str] = None, webpack_url: str = None) -> ParamsData:
        logger.info("Reloading requests params data...")
        self.script_srcs = script_srcs or self.script_srcs
        self.webpack_url = webpack_url or self.webpack_url
        result = self._load_from_web_and_save()

        return {key: RequestParams(**value) for key, value in result.items()}
