# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class ShelterPatient(models.Model):
    _name = 'shelter.patient'
    _description = 'Patient'
    _inherit = ['mail.thread', 'images.mixin']

    name = fields.Char(string='Name', required=True, help='The name of the patient')
    species_id = fields.Many2one('shelter.animal.species', required=True)
    crossbreed = fields.Boolean('Crossbreed')
    purebred_breed_id = fields.Many2one('shelter.animal.species.breed', string='Purebred breed', domain="[('species_id', '=', species_id)]")
    crossbreed_breed_ids = fields.Many2many('shelter.animal.species.breed', string='Crossbreed breeds', domain="[('species_id', '=', species_id)]")
    owner_id = fields.Many2one('res.partner', string='Owner')
    contact_ids = fields.One2many('shelter.patient.contact', 'patient_id', 'Contacts')
    fallback_image = fields.Binary('Fallback Image', compute='_compute_fallback_image', inverse='_inverse_fallback_image')
    fallback_image_small = fields.Binary('Image small', compute='_compute_fallback_image_small')
    fallback_image_medium = fields.Binary('Image medium', compute='_compute_fallback_image_medium')

    @api.constrains('purebred_breed_id', 'crossbreed_breed_ids')
    def _check_breed(self):
        for patient in self:
            if (patient.purebred_breed_id or not patient.crossbreed) and (patient.crossbreed_breed_ids or patient.crossbreed):
                raise ValidationError(_('An animal cannot be purebred and crossbreed'))

    @api.constrains('species_id', 'purebred_breed_id', 'crossbreed_breed_ids')
    def _check_species_breed(self):
        for patient in self:
            if any(breed.species_id != patient.species_id for breed in set(patient.purebred_breed_id + patient.crossbreed_breed_ids)):
                raise ValidationError(_('An animal cannot have a breed from a different species than its own species'))

    @api.depends('image', 'species_id.image', 'purebred_breed_id.image')
    def _compute_fallback_image(self):
        for patient in self:
            patient.fallback_image = patient.image or patient.purebred_breed_id.image or patient.species_id.image

    @api.depends('image_small', 'species_id.image_small', 'purebred_breed_id.image_small')
    def _compute_fallback_image_small(self):
        for patient in self:
            patient.fallback_image_small = patient.image_small or patient.purebred_breed_id.image_small or patient.species_id.image_small

    @api.depends('image_medium', 'species_id.image_medium', 'purebred_breed_id.image_medium')
    def _compute_fallback_image_medium(self):
        for patient in self:
            patient.fallback_image_medium = patient.image_medium or patient.purebred_breed_id.image_medium or patient.species_id.image_medium

    def _inverse_fallback_image(self):
        for record in self:
            vals = {'image': record.fallback_image}
            tools.image_resize_images(vals)
            record.image = vals['image']
            record.image_small = vals['image_small']
            record.image_medium = vals['image_medium']

    @api.onchange('purebred_breed_id', 'crossbreed_breed_ids')
    def onchange_breed(self):
        if self.purebred_breed_id:
            self.crossbreed = False
        elif self.crossbreed_breed_ids:
            self.crossbreed = True

    @api.onchange('species_id')
    def onchange_species(self):
        if self.species_id:
            if self.purebred_breed_id.species_id != self.species_id:
                self.purebred_breed_id = None
            if any(breed.species_id != self.species_id for breed in self.crossbreed_breed_ids):
                self.crossbreed_breed_ids = self.crossbreed_breed_ids.filtered(lambda b: b.species_id == self.species_id)


class ShelterPatientContact(models.Model):
    _name = 'shelter.patient.contact'
    _description = 'Patient Contact'

    partner_id = fields.Many2one('res.partner', required=True)
    patient_id = fields.Many2one('shelter.patient', required=True)
    type = fields.Many2one('shelter.patient.contact.type')


class ShelterPatientContactType(models.Model):
    _name = 'shelter.patient.contact.type'
    _description = 'Patient Contact Type'

    name = fields.Char(string='Name', required=True)
