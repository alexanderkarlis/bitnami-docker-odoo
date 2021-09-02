# -*- coding: utf-8 -*-

from odoo import models, fields, api
from enum import Enum
import logging

class SimsAccount(models.Model):
        _name = 'sims.account'
        _description = 'SIMS Account'

        policy_name = fields.Char(required=True, help=u'Policy Number or Policy Name')   
        effective_date = fields.Date()
        expiration_date = fields.Date()
 
        insured_id  = fields.Many2one(comodel_name='res.partner')
        insured_contact_id = fields.Many2one(comodel_name='res.partner')
        producer_id  = fields.Many2one(comodel_name='res.partner')
        producer_contact_id = fields.Many2one(comodel_name='res.partner')
        underwriter_id = fields.Many2one(comodel_name='res.partner')
        underwriter_contact_id = fields.Many2one(comodel_name='res.partner')

        telematics_id  = fields.Char(help=u'Telematics Group Id')               #  matches a telematics vendor group id
        telematics_group_name = fields.Char(help=u'Telematics Group Name')      #  matches a telematics vendor group name
        start_date = fields.Date(help=u'start date of service')                 #  start of telematics account (typically ~month after effective)
        end_date = fields.Date(help=u'end date of service')                     #  end of telematics account   (typically on expiration/renewal)

        vehicles = fields.One2many(comodel_name='sims.vehicle', inverse_name='sims_account_id')
        drivers = fields.One2many(comodel_name='sims.driver', inverse_name='sims_account_id')

        vehicle_count = fields.Integer(compute='_vehicle_count')
        driver_count = fields.Integer(compute='_driver_count')

        _sql_constraints = [
                ('policy_name_unique',
                'UNIQUE(policy_name)',
                "The policy name must be unique."),
        ]

        insured_name = fields.Char(related="insured_id.name", readonly=True)

        @api.depends('vehicles')
        def _vehicle_count(self):
                for r in self:
                        r.vehicle_count = len(self.env['sims.vehicle'].search([('sims_account_id','=', r.id)]).ids)
        
        @api.depends('drivers')
        def _driver_count(self):
                for r in self:
                        r.driver_count = len(self.env['sims.driver'].search([('sims_account_id','=', r.id)]).ids)




class SimsVehicle(models.Model):
        _name = 'sims.vehicle'
        _description = 'SIMS Vehicle'
        name = fields.Char()
        year = fields.Integer()
        make = fields.Char()
        model = fields.Char()
        vin  = fields.Char()
        gvw = fields.Integer()
        radius = fields.Integer()
        # garage_address_id = fields.Many2one(related='res.partner')
        status = fields.Selection(selection=[('active','Active'), ('inactive','Inactive')])
        sims_account_id  = fields.Many2one(comodel_name='sims.account')
        telematics_id = fields.Char()
        telematics_vehicle_name = fields.Char()


class SimsDriver(models.Model):
        _name = 'sims.driver'
        _description = 'SIMS Driver'
        name_first = fields.Char()
        name_last = fields.Char()
        email = fields.Char()
        license_number = fields.Char()
        license_state = fields.Many2one(comodel_name='res.country.state')
        sims_account_id = fields.Many2one(comodel_name='sims.account')
        telematics_id = fields.Char()
        status = fields.Selection(selection=[('active', 'Active'), ('inactive', 'Inactive')])
