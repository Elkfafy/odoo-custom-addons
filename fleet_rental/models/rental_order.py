from odoo import models, fields, api, _

class RentalOrder(models.Model):
    # basic information
    _name = 'rental.order'
    _inherits = {
                    'fleet.vehicle': 'vehicle_id',
                }
    vehicle_id = fields.Many2one('fleet.vehicle', string=_("Vehicle"), domain="[['state_id.name', '=', 'Registered']]")
    contract_id = fields.Many2one('fleet.vehicle.log.contract', string="Contract", required=False)
    driver_id = fields.Many2one(
        'res.partner', 
        required=True, 
        string=_("Driver", ar="السواق"),
        domain=[]
    )
    state = fields.Selection(selection=[('op_dep', "Operation Department"), 
                                        ('tr_dep', "Transfer Department"),
                                        ('mo_dep', 'Monetary Department'),
                                        ('ge_dep', "General Manager"),
                                        ('in_progress', "Compelete"),
                                        ("rejected", "Rejected")],
                                        default='op_dep',
                                        string="status")
    # vin_sn = fields.Char(string="chassis Number", related='vehicle_id.vin_sn', readonly=False)
    tags = fields.Many2many('fleet.vehicle.tag', 
                            string="Status", 
                            related='vehicle_id.tag_ids',
                            readonly=False)
    # driver information
    driver_license = fields.Binary(string="Driver License", required=True, attachment=True)
    driver_employment = fields.Binary(string="Driver Employment", required=True, attachment=True)
    driver_residence = fields.Binary(string="Driver ID", attachment=True)
    driver_license_name = fields.Char()
    driver_employment_name = fields.Char()
    driver_residence_name = fields.Char()
    # rental information
    rental_start = fields.Date(string="Start Date", required=True,readonly=False, compute="_compute_rental_start_input", inverse="_inverse_rental_start_input")
    rental_start_input = fields.Date()
    rental_end = fields.Date(string="End Date", required=True, readonly=False, compute="_compute_rental_end_input", inverse="_inverse_rental_end_input")
    rental_end_input = fields.Date()
    rental_type = fields.Selection(
        selection='_get_rental_type_selection',
        string="Rental Type", 
        readonly=False,
        required=True,
        compute="_compute_rental_type_input",
        inverse="_inverse_rental_type_input"
    )
    rental_type_input = fields.Selection(selection='_get_rental_type_selection')
    # cost information
    activation_cost = fields.Monetary(string="Activation Cost", related="contract_id.amount", readonly=False)
    recurring_cost = fields.Monetary(string="Recurring Cost", related="contract_id.cost_generated", readonly=False)

    # Rejection Information
    reject_reason = fields.Text(string=_("Rejection Reason"))

    @api.depends('state')
    def accept_order(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>. accept order")
        next_states = {
            'op_dep': lambda rec: 'tr_dep',
            'tr_dep': self.transaction_department_accept,
            'mo_dep': lambda rec: 'ge_dep',
            'ge_dep': self.general_department_accept,
            'in_progress': lambda rec: 'in_progress',
            'rejected': lambda rec: 'rejected'
        }
        for rec in self:
            rec.state = next_states[rec.state](rec)

    def reject_order(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>reject, from odoo")
        for rec in self:
            if rec.state != 'in_progress':
                rec.state = 'rejected'

###### inner methods ######
    # def operation_department_accept(self):
    #     return 'tr_dep'
    def transaction_department_accept(self, rec):
        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>> {rec.rental_start_input}")
        contract = self.env['fleet.vehicle.log.contract']
        new_contract = {
            'vehicle_id': rec.vehicle_id.id,
            'cost_frequency': rec.rental_type,
            'start_date': rec.rental_start,
            'expiration_date': rec.rental_end,
        }
        rec.contract_id = contract.create(new_contract)
        return 'mo_dep'
    
    def general_department_accept(self, rec):
        state = self.env['fleet.vehicle.state'].search([('name', '=', 'Rented')])
        if (not state):
            state = self.env['fleet.vehicle.state'].create({'name': 'Rented'})
        else:
            state = state[0]
        rec.vehicle_id.state_id = state.id
        rec.vehicle_id.driver_id = rec.driver_id.id
        return 'in_progress'

    @api.model
    def execute_daily_expiration_checker(self):
        for rec in self:
            if rec.contract_id.state == 'expired':
                body='hello from odoo'
                subject='this is odoo minut repeating testing'
                recipient_email = 'hmdeslam.adel@gmail.com'
                email_values = {
            'subject': subject,
            'body_html': body,
            'email_to': recipient_email,
        }
            email = self.env['mail.mail'].create(email_values)

            # Link the email to your model (optional)
            self.message_post(body=body, subject=subject, subtype='mail.mt_comment', message_type='email',
                            email_from=email.email_from, email_to=email.email_to, email_cc=email.email_cc,
                            email_bcc=email.email_bcc)

            return email.id
                    # self.message_post(
                    #     body='hello from odoo',
                    #     subject='this is odoo minut repeating testing',
                    #     subtype='mail.mt_comment',
                    #     message_type='email',
                    #     email_from=
                    # )

############## compute and inverse methods ####################
    ############# rental start ###################
    @api.depends('contract_id', 'contract_id.expiration_date')
    def _compute_rental_start_input(self):
        for rec in self:
            if rec.contract_id:
                rec.rental_start = rec.contract_id.start_date
            else:
                rec.rental_start = rec.rental_start_input
    
    @api.depends("rental_start", "rental_start_input")
    def _inverse_rental_start_input(self):
        for rec in self:
            if rec.contract_id:
                rec.contract_id.start_date = rec.rental_start
            else:
                rec.rental_start_input = rec.rental_start

    ############# rental end ###################
    @api.depends("contract_id", "contract_id.expiration_date")
    def _compute_rental_end_input(self):
        for rec in self:
            if rec.contract_id:
                rec.rental_end = rec.contract_id.expiration_date
            else:
                rec.rental_end = rec.rental_end_input

    @api.depends("rental_end", "rental_end_input")
    def _inverse_rental_end_input(self):
        for rec in self:
            if rec.contract_id:
                rec.contract_id.expiration_date = rec.rental_end
            else:
                rec.rental_end_input = rec.rental_end

    ############# rental type ###################
    @api.depends("contract_id", "contract_id.cost_frequency")
    def _compute_rental_type_input(self):
        for rec in self:
            rec.rental_type = self.contract_id.cost_frequency
            if rec.contract_id:
                rec.rental_type = rec.contract_id.cost_frequency
            else:
                rec.rental_type = rec.rental_type_input

    @api.depends("rental_type", "rental_type_input")
    def _inverse_rental_type_input(self):
        for rec in self:
            if rec.contract_id:
                rec.contract_id.cost_frequency = rec.rental_type
            else:
                rec.rental_type_input = rec.rental_type

    def _get_rental_type_selection(self):
        selections = self.env['ir.model.fields'].search(domain=[("name", "=", "cost_frequency")], limit=1)[0].selection_ids
        alist = []
        for selection in selections:
            alist.append((selection.value, selection.name))
        return alist