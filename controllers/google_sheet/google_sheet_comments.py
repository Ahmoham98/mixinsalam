
from schema.google_sheet.comments import Comment
from google_sheet_configuration import spreadsheet
from schema.google_sheet.google_sheet_users import Users
from utils import utilities


class CommentsController:
    sheet = spreadsheet.worksheet("comments")

    @staticmethod
    async def get_all_comments():
        records = CommentsController.sheet.get_all_records()
        return records

    @staticmethod
    async def get_comment_by_id(comment_id: int):
        records = CommentsController.sheet.get_all_records()
        for record in records:
            if int(record["id"]) == comment_id:
                return record
        return None

    @staticmethod
    async def create_comment(comment: Comment, user: Users):
        sheet = CommentsController.sheet
        next_id = await utilities.get_next_id(sheet)
        user_id = user["id"]
        status = "open"
        CommentsController.sheet.append_row([
            next_id, user_id, comment.title, comment.comment, status
        ])
        return {"message": "Comment created successfully"}

    @staticmethod
    async def update_comment(comment_id: int, comment: Comment, user: Users):
        records = CommentsController.sheet.get_all_records()
        user_id = user["id"]
        for idx, record in enumerate(records, start=2):
            if int(record["id"]) == comment_id:
                CommentsController.sheet.update(f"A{idx}:E{idx}", [[
                    comment_id, user_id, comment.title, comment.comment
                ]])
                return {"message": "Comment updated successfully"}
        return {"error": "Comment not found"}

    @staticmethod
    async def delete_comment(comment_id: int):
        records = CommentsController.sheet.get_all_records()
        for idx, record in enumerate(records, start=2):
            if int(record["id"]) == comment_id:
                CommentsController.sheet.delete_rows(idx)
                return {"message": "Comment deleted successfully"}
        return {"error": "Comment not found"}