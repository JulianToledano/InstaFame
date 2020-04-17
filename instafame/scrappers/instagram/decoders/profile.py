
class ProfileEncoder:
    def decode(self, follower):
        result = {}
        result['biography'] = follower.biography
        result['followees'] = follower.followees
        result['followers'] = follower.followers
        result['full_name'] = follower.full_name
        result['igtvcount'] = follower.igtvcount
        result['is_private'] = follower.is_private
        result['is_verified'] = follower.is_verified
        result['mediacount'] = follower.mediacount
        result['userid'] = follower.userid
        result['username'] = follower.username
        result['_iphone_struct'] = follower._iphone_struct
        result['_iphone_struct_'] = follower._iphone_struct_
        return result