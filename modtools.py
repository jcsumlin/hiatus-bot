class ModTools:
    pretext = 'Hey there %s this post has been removed in accordance to rule %s:\r\r'
    reasons = ['**No low-effort posts**. Do not post simple memes, screenshots, or unaffiliated images. '
               + 'Keep content related to Star VS the Forces of Evil.',
               'Don\'t repost something unless 90 days have passed.',
               'NSFW content is **NOT** allowed. This includes suggestive images, jokes, etc.',
               'Mark posts as spoilers if needed until the Monday after premiering. Keep spoilers for new episodes out of ' +
               'post titles. [Click here for info regarding spoiler formatting](https://www.reddit.com/r/StarVStheForcesofEvil/wiki/markdown). Leaked content is **not** allowed.',
               'No illegal streaming links. Support the show by watching via official methods. Episode links are provided' +
               'in each discussion thread for viewers in countries with no legal way to watch.',
               'Be nice! Don\'t insult other users, fandoms, etc.']
    post_text = '\r\rIf you have any questions please [message the moderators](https://www.reddit.com/message/compose?to=%2Fr%2FStarVStheForcesofEvil&subject=&message=)'

    def __init__(self):
        self.reason = ""
        self.user = ""
        pass

    def remove_alert(self, reason, user):
        self.reason = reason
        self.user = user
        if "low-effort" in self.reason:
            return (self.pretext % (self.user, '2')) + self.reasons[0] + self.post_text
        elif "repost" in self.reason:
            return (self.pretext % (self.user, '3')) + self.reasons[1] + self.post_text
        elif "nsfw" in self.reason:
            return (self.pretext % (self.user, '5')) + self.reasons[2] + self.post_text
        elif "spoiler" in self.reason:
            return (self.pretext % (self.user, '6')) + self.reasons[3] + self.post_text
        elif "illegal" in self.reason:
            return (self.pretext % (self.user, '7')) + self.reasons[4] + self.post_text
        elif "nice" in self.reason:
            return (self.pretext % (self.user, '8')) + self.reasons[5] + self.post_text


