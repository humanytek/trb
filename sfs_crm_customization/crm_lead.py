# -*- encoding: utf-8 -*
##############################################################################
#
#    Copyright (c) 2013 SF Soluciones.
#    (http://www.sfsoluciones.com)
#    contacto@sfsoluciones.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields,osv
from openerp.addons.base_status.base_stage import base_stage
from base.res.res_partner import format_address

class crm_lead(base_stage, format_address, osv.osv):
    
    _inherit = "crm.lead"
    _columns = {
                'meeting_ids': fields.one2many("crm.meeting", "opportunity_id", "Meetings To be held")
                }

    def log_meeting(self, cr, uid, ids, meeting_subject, meeting_date, duration, context=None):
          if context == None:
              context = {}
          if context.get('meeting_id'):
              return self.write(cr, uid, ids, {'meeting_ids': 
                                               [(4,context['meeting_id'])]},context=context)

crm_lead()

class crm_meeting(osv.Model):
    
    _inherit = 'crm.meeting'
    
    def create(self, cr, uid, vals, context=None):
        res = super(crm_meeting, self).create(cr, uid, vals, context=context)
        obj = self.browse(cr, uid, res, context=context)
        if obj.opportunity_id:
            context.update({'meeting_id' : obj.id })
            self.pool.get('crm.lead').log_meeting(cr, uid, [obj.opportunity_id.id], obj.name, obj.date, obj.duration, context=context)
        return res

crm_meeting()
             
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:-