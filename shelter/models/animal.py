# -*- coding: utf-8 -*-

from odoo import fields, models


class ShelterAnimalSpecies(models.Model):
    _name = 'shelter.animal.species'
    _inherit = ['images.mixin']
    _description = 'Species'

    name = fields.Char(string='Name', required=True)


class ShelterAnimalSpeciesBreed(models.Model):
    _name = 'shelter.animal.species.breed'
    _inherit = ['images.mixin']
    _description = 'Species breed'

    name = fields.Char(string='Name', required=True)
    species_id = fields.Many2one('shelter.animal.species', required=True)
