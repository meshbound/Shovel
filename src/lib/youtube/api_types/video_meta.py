class VideoMeta:
    def __init__(self,
                 video_path: str,
                 title: str = "Title", 
                 description: str = "Description",
                 privacy_status: str = "private", 
                 tags: [str] = [], 
                 default_language: str = "en-US",
                 embeddable: bool = True,
                 public_stats: bool = True,
                 for_kids: bool = False) -> None:
        self.video_path = video_path
        self.title = title
        self.description = description
        self.privacy_status = privacy_status
        self.tags = tags
        self.default_language = default_language
        self.embeddable = embeddable
        self.public_stats = public_stats
        self.for_kids = for_kids
