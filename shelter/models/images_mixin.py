# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools


class ImagesMixin(models.AbstractModel):
    _name = 'images.mixin'
    _description = 'Images Mixin'

    image = fields.Binary('Image', attachment=True)
    image_medium = fields.Binary('Medium-sized image', attachment=True,)
    image_small = fields.Binary('Small-sized image', attachment=True,)

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(ImagesMixin, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(ImagesMixin, self).write(vals)
