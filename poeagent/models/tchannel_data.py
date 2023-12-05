class TchannelData:
    def __init__(self, **kwargs):
        self.minSeq = kwargs.get("minSeq")
        self.channel = kwargs.get("channel")
        self.channelHash = kwargs.get("channelHash")
        self.boxName = kwargs.get("boxName")
        self.baseHost = kwargs.get("baseHost")
        self.targetUrl = kwargs.get("targetUrl")
        self.enableWebsocket = kwargs.get("enableWebsocket")
