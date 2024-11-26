from odoo import api, fields, models, SUPERUSER_ID


class MailChannel(models.Model):
    _inherit = "mail.channel"

    matrix_room_id = fields.Char(index=True)

    # TODO: unique

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, *args, **kwargs):
        message = super(MailChannel, self).message_post(*args, **kwargs)

        matrix_room_id = self.matrix_room_id
        if self.matrix_room_id:
            guests = self.channel_last_seen_partner_ids.mapped("guest_id")

            # exclude self
            guests -= message.author_guest_id

            matrix_bot_ids = guests.ids
            if not matrix_bot_ids:
                return message

        author = message.author_id.display_name
        body = tools.html2plaintext(message.body)
        _context = message.env.context

        @self.env.cr.postcommit.add
        def send_notifications():
            db_registry = registry(dbname)
            with db_registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, _context)
                bots = env['matrix.bot'].browse(matrix_bot_ids)
                for bot in bots:
                    bot._message_post(room_id=matrix_room_id, author=author, body=body)

        return message
