# -*- coding: utf-8 -*-
# from odoo import http


# class Custom-delivery(http.Controller):
#     @http.route('/custom-delivery/custom-delivery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom-delivery/custom-delivery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom-delivery.listing', {
#             'root': '/custom-delivery/custom-delivery',
#             'objects': http.request.env['custom-delivery.custom-delivery'].search([]),
#         })

#     @http.route('/custom-delivery/custom-delivery/objects/<model("custom-delivery.custom-delivery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom-delivery.object', {
#             'object': obj
#         })

