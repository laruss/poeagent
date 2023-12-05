import logging
import re

from bs4 import BeautifulSoup
from js2py import eval_js
from requests import get

from .requests_params import RequestsParams, ParamsData
from .utils import get_resource

logger = logging.getLogger(__name__)


class JS:
    js_file = "tag_id.js"
    tag_js_script = get_resource(js_file)
    tag_js_script_function_name = "mySuper.puper"

    form_key_pattern = r"window\.([a-zA-Z0-9]+)=function\(\)\{return window"
    tag_id_method_pattern = r"let getAPISig=\([^)]*\)=>window\.([^(]*)"
    window_secret_pattern = r'let useFormkeyDecode=[\s\S]*?(window\.[\w]+="[^"]+")'
    static_pattern = r'static[^"]*\.js'

    def __init__(self, document: str):
        self._window = "const window={document:{hack:1},navigator:{userAgent:'safari <3'}};"
        self._src_scripts = []
        self._webpack_script: str = None
        self._tag_id_method_name = None

        self.__init_window(document)
        self.requests_params = RequestsParams(self._src_scripts, self._webpack_script)

    def __init_window(self, document: str):
        """ initialize the window object with document scripts """
        logger.info("Initializing window")

        scripts = BeautifulSoup(document, "html.parser").find_all('script')
        for script in scripts:
            if (src := script.attrs.get("src")) and (src not in self._src_scripts):
                if "_app" in src:
                    self.__init_app(src)
                if "buildManifest" in src:
                    self.__extend_src_scripts(src)
                elif "webpack" in src:
                    self._webpack_script = src
                    self.__extend_src_scripts(src)
                else:
                    self._src_scripts.append(src)
            elif ("document." in script.text) or ("function" not in script.text):
                continue
            elif script.attrs.get("type") == "application/json":
                continue
            self._window += script.text

        logger.info("Window initialized")

    def __init_app(self, src: str):
        script = self.__load_src_script(src)
        if not (tag_id_match := re.search(self.tag_id_method_pattern, script)):
            raise RuntimeError("Failed to find tag_id method name in js scripts")
        if not (window_secret_match := re.search(self.window_secret_pattern, script)):
            raise RuntimeError("Failed to find window secret in js scripts")

        self._tag_id_method_name = tag_id_match.group(1)
        self._window += window_secret_match.group(1) + ';'

    def __extend_src_scripts(self, manifest_src: str):
        """ extend src scripts list with static scripts from manifest """
        static_main_url = self.__get_base_url(manifest_src)
        manifest = self.__load_src_script(manifest_src)

        matches = re.findall(self.static_pattern, manifest)
        scr_list = [f"{static_main_url}{match}" for match in matches]

        self._src_scripts.extend(scr_list)

    @staticmethod
    def __load_src_script(src: str) -> str:
        resp = get(src)
        if resp.status_code != 200:
            logger.warning(f"Failed to load script {src}, status code: {resp.status_code}")

        return resp.text

    @staticmethod
    def __get_base_url(src: str) -> str:
        return src.split("static/")[0]

    def get_form_key(self) -> str:
        script = self._window

        match = re.search(self.form_key_pattern, script)
        if not (secret := match.group(1)):
            raise RuntimeError("Failed to parse form-key function in Poe document")

        script += f'window.{secret}().slice(0, 32);'

        return str(eval_js(script))

    def get_tag_id(self, form_key: str, data: str) -> str:
        script = self._window
        script += self.tag_js_script + f"window.{self._tag_id_method_name}" + \
            f"({self.tag_js_script_function_name}, '{form_key}', '{data}');"

        return str(eval_js(script))

    def reload_requests_params(self, document: str) -> ParamsData:
        self.__init_window(document)
        return self.requests_params.reload(self._src_scripts, self._webpack_script)
