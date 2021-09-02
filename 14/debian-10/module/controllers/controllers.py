# -*- coding: utf-8 -*-
from odoo import http


class Sims_Controller(http.Controller):
    @http.route('/sims/sims/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/sims/sims/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('sims.listing', {
            'root': '/sims/sims',
            'objects': http.request.env['sims.sims'].search([]),
        })

    @http.route('/sims/sims/objects/<model("sims.sims"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('sims.object', {
            'object': obj
        })
