# Copyright 2015 ABF OSIELL <https://osiell.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.http import request
import werkzeug


class AuditlogtHTTPSession(models.Model):
    _name = "auditlog.http.session"
    _description = "Auditlog - HTTP User session log"
    _order = "create_date DESC"

    display_name = fields.Char("Name", compute="_compute_display_name", store=True)
    name = fields.Char("Session ID", index=True)
    user_id = fields.Many2one("res.users", string="User", index=True)
    ip_address = fields.Char("IP Address", help="IP address of the user session")
    http_request_ids = fields.One2many(
        "auditlog.http.request", "http_session_id", string="HTTP Requests"
    )

    @api.depends("create_date", "user_id")
    def _compute_display_name(self):
        for httpsession in self:
            create_date = fields.Datetime.from_string(httpsession.create_date)
            tz_create_date = fields.Datetime.context_timestamp(httpsession, create_date)
            httpsession.display_name = "{} ({})".format(
                httpsession.user_id and httpsession.user_id.name or "?",
                fields.Datetime.to_string(tz_create_date),
            )

    def name_get(self):
        return [(session.id, session.display_name) for session in self]

    @api.model
    def current_http_session(self):
        """Create a log corresponding to the current HTTP user session, and
        returns its ID. This method can be called several times during the
        HTTP query/response cycle, it will only log the user session on the
        first call.
        If no HTTP user session is available, returns `False`.
        """
        if not request:
            return False
        httpsession = request.session
        if httpsession:
            try:
                # obtener ip del cliente (session)
                ip_address = request.httprequest.remote_addr
            except Exception:
                ip_address = '0.0.0.0'

            existing_session = self.search(
                [("name", "=", httpsession.sid), ("user_id", "=", request.uid), ("ip_address", "=", httpsession.sip_address)], limit=1
            )
            if existing_session:
                return existing_session.id
            vals = {"name": httpsession.sid, "user_id": request.uid ,"ip_address": ip_address}
            httpsession.auditlog_http_session_id = self.create(vals).id
            return httpsession.auditlog_http_session_id
        return False
