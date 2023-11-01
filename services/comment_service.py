from models.comment import Comment, CommentModel

class CommentService:

    def __init__(self, repository: CommentModel):
        self.repository = repository


    def comment_post(self, post_id, content, content_timestamp):
        new_comment = Comment(post_id=post_id, content=content, content_timestamp=content_timestamp)
        self.repository.add_comment(new_comment)

    
    def seriakize_comment(self, comment):
        return {
        "id": comment.id,
        "post_id": comment.post_id,
        "content": comment.content,
        "content_timestamp": comment.content_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }

