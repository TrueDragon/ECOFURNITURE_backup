from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm, CreateCustomerForm, CreateFurnitureForm, PaymentForm, ReportForm, OrderForm
import shelve
import User
import Customer
import Furniture
import Pay
import Order
import Report

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

# THIS IS FOR LINKING NAVBAR IN PRODUCT WEBSITE #
@app.route('/products')
def products():
    return render_template('products.html')


@app.route('/living_room')
def living_room():
    return app.send_static_file('living_room.html')


@app.route('/bedroom')
def bedroom():
    return app.send_static_file('bedroom.html')


@app.route('/contact_us')
def contact():
    return app.send_static_file('contact_us.html')


@app.route('/dining_room')
def dining_room():
    return app.send_static_file('dining_room.html')


@app.route('/light')
def light():
    return app.send_static_file('light.html')


@app.route('/office')
def office():
    return app.send_static_file('office.html')


@app.route('/account')
def account():
    return app.send_static_file('account.html')

# END OF LINKING NAVBAR #

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
                         create_user_form.gender.data, create_user_form.membership.data,
                         create_user_form.remarks.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        db.close()

        return redirect(url_for('retrieve_users'))
    return render_template('createUser.html', form=create_user_form)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                     create_customer_form.gender.data, create_customer_form.membership.data,
                                     create_customer_form.remarks.data, create_customer_form.email.data,
                                     create_customer_form.date_joined.data, create_customer_form.address.data)
# customers_dict[customer.get_customer_id()] = customer
        customers_dict[customer.get_user_id()] = customer
        db['Customers'] = customers_dict

        db.close()

        return redirect(url_for('retrieve_customers'))
    return render_template('createCustomer.html', form=create_customer_form)


@app.route('/createFurniture', methods=['GET', 'POST'])
def create_furniture():
    create_furniture_form = CreateFurnitureForm(request.form)
    if request.method == 'POST' and create_furniture_form.validate():
        furniture_dict = {}
        db = shelve.open('furniture.db', 'c')

        try:
            furniture_dict = db['Furniture']
        except:
            print("Error in retrieving Users from user.db.")

        furniture = Furniture.Furniture(create_furniture_form.furniture_type.data, create_furniture_form.furniture_quantity.data,
                                        create_furniture_form.furniture_category.data, create_furniture_form.furniture_status.data,
                                        create_furniture_form.furniture_price.data, create_furniture_form.furniture_remarks.data)
        furniture_dict[furniture.get_furniture_id()] = furniture
        db['Furniture'] = furniture_dict

        db.close()

        return redirect(url_for('retrieve_furniture'))
    return render_template('createFurniture.html', form=create_furniture_form)


@app.route('/createpayment', methods=['GET', 'POST'])
def payment():
    payment_form = PaymentForm(request.form)
    if request.method == 'POST' and payment_form.validate():
        payment_dict = {}
        db = shelve.open('payment.db', 'c')

        try:
            payment_dict = db['Info']
        except:
            print("Error in retrieving Users from user.db.")

        payment = Pay.Payment(payment_form.first_name.data, payment_form.last_name.data, payment_form.card_no.data,
                              payment_form.exp.data, payment_form.cvv.data)

        payment_dict[payment.get_cust_id()] = payment
        db['Info'] = payment_dict

        db.close()

        return redirect(url_for('retrieve_payment'))
    return render_template('createpayment.html', form=payment_form)


@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)


@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)


@app.route('/retrieveFurniture')
def retrieve_furniture():
    furniture_dict = {}
    db = shelve.open('furniture.db', 'r')
    furniture_dict = db['Furniture']
    db.close()

    furniture_list = []
    for key in furniture_dict.keys():
        furniture = furniture_dict.get(key)
        furniture_list.append(furniture)

    return render_template('retrieveFurniture.html', count=len(furniture_list), furniture_list=furniture_list)


@app.route('/retrievePayment')
def retrieve_payment():
    payment_dict = {}
    db = shelve.open('payment.db', 'r')
    payment_dict = db['Info']
    db.close()

    payment_list = []
    for key in payment_dict.keys():
        payment = payment_dict.get(key)
        payment_list.append(payment)

    return render_template('retrievePayment.html', count=len(payment_list), payment_list=payment_list)


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_membership(update_user_form.membership.data)
        user.set_remarks(update_user_form.remarks.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.membership.data = user.get_membership()
        update_user_form.remarks.data = user.get_remarks()

        return render_template('updateUser.html', form=update_user_form)


@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_date_joined(update_customer_form.date_joined.data)
        customer.set_address(update_customer_form.address.data)
        customer.set_membership(update_customer_form.membership.data)
        customer.set_remarks(update_customer_form.remarks.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.date_joined.data = customer.get_date_joined()
        update_customer_form.address.data = customer.get_address()
        update_customer_form.membership.data = customer.get_membership()
        update_customer_form.remarks.data = customer.get_remarks()

        return render_template('updateCustomer.html', form=update_customer_form)


@app.route('/updateFurniture/<int:id>/', methods=['GET', 'POST'])
def update_furniture(id):
    update_furniture_form = CreateFurnitureForm(request.form)
    if request.method == 'POST' and update_furniture_form.validate():
        furniture_dict = {}
        db = shelve.open('furniture.db', 'w')
        furniture_dict = db['Furniture']

        furniture = furniture_dict.get(id)
        furniture.set_furniture_type(update_furniture_form.furniture_type.data)
        furniture.set_furniture_quantity(
            update_furniture_form.furniture_quantity.data)
        furniture.set_furniture_category(
            update_furniture_form.furniture_category.data)
        furniture.set_furniture_status(
            update_furniture_form.furniture_status.data)
        furniture.set_furniture_price(
            update_furniture_form.furniture_price.data)
        furniture.set_furniture_remarks(
            update_furniture_form.furniture_remarks.data)

        db['Furniture'] = furniture_dict
        db.close()

        return redirect(url_for('retrieve_furniture'))

    else:
        furniture_dict = {}
        db = shelve.open('furniture.db', 'r')
        furniture_dict = db['Furniture']
        db.close()

        furniture = furniture_dict.get(id)
        update_furniture_form.furniture_type.data = furniture.get_furniture_type()
        update_furniture_form.furniture_quantity.data = furniture.get_furniture_quantity()
        update_furniture_form.furniture_category.data = furniture.get_furniture_category()
        update_furniture_form.furniture_status.data = furniture.get_furniture_status()
        update_furniture_form.furniture_price.data = furniture.get_furniture_price()
        update_furniture_form.furniture_remarks.data = furniture.get_furniture_remarks()

        return render_template('updateFurniture.html', form=update_furniture_form)


@app.route('/updatePayment/<int:id>/', methods=['GET', 'POST'])
def update_payment(id):
    update_payment_form = PaymentForm(request.form)
    if request.method == 'POST' and update_payment_form.validate():
        payment_dict = {}
        db = shelve.open('payment.db', 'w')
        payment_dict = db['Info']

        payment = payment_dict.get(id)
        payment.set_first_name(update_payment_form.first_name.data)
        payment.set_last_name(update_payment_form.last_name.data)
        payment.set_card_no(update_payment_form.card_no.data)
        payment.set_exp(update_payment_form.exp.data)
        payment.set_cvv(update_payment_form.cvv.data)

        db['Info'] = payment_dict
        db.close()

        return redirect(url_for('retrieve_payment'))

    else:
        payment_dict = {}
        db = shelve.open('payment.db', 'r')
        payment_dict = db['Info']
        db.close()

        payment = payment_dict.get(id)
        update_payment_form.first_name.data = payment.get_first_name()
        update_payment_form.last_name.data = payment.get_last_name()
        update_payment_form.card_no.data = payment.get_card_no()
        update_payment_form.exp.data = payment.get_exp()
        update_payment_form.cvv.data = payment.get_cvv()
        return render_template('updatePayment.html', form=update_payment_form)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))


@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']
    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('retrieve_customers'))


@app.route('/deleteFurniture/<int:id>', methods=['POST'])
def delete_furniture(id):
    furniture_dict = {}
    db = shelve.open('furniture.db', 'w')
    furniture_dict = db['Furniture']

    furniture_dict.pop(id)

    db['Furniture'] = furniture_dict
    db.close()

    return redirect(url_for('retrieve_furniture'))


@app.route('/deletePayment/<int:id>', methods=['POST'])
def delete_payment(id):
    payment_dict = {}
    db = shelve.open('payment.db', 'w')
    payment_dict = db['Info']

    payment_dict.pop(id)

    db['Info'] = payment_dict
    db.close()

    return redirect(url_for('retrieve_payment'))


@app.route('/createOrder', methods=['GET', 'POST'])
def create_order():
    create_order_form = OrderForm(request.form)
    if request.method == 'POST' and create_order_form.validate():
        orders_dict = {}
        db = shelve.open('order.db', 'c')

        try:
            orders_dict = db['Orders']
        except:
            print("Error in retriving Orders from order.db")

        order = Order.Order(create_order_form.customer_id.data, create_order_form.order_id.data,
                            create_order_form.item_id.data, create_order_form.item_quantity.data)
        orders_dict[order.get_customer_id()] = order
        db['Orders'] = orders_dict

        db.close()
        return redirect(url_for('retrieve_orders'))
    return render_template('createOrder.html', form=create_order_form)


@app.route('/retrieveOrders')
def retrieve_orders():
    orders_dict = {}
    db = shelve.open('order.db', 'r')
    orders_dict = db['Orders']
    db.close()

    orders_list = []
    for key in orders_dict:
        order = orders_dict.get(key)
        orders_list.append(order)

    return render_template('retrieveOrders.html', count=len(orders_list), orders_list=orders_list)


@app.route('/updateOrder/<id>', methods=['GET', 'POST'])
def update_order(id):
    update_order_form = OrderForm(request.form)
    if request.method == 'POST' and update_order_form.validate():
        orders_dict = {}
        db = shelve.open('order.db', 'w')
        orders_dict = db['Orders']

        order = orders_dict.get(id)
        order.set_customer_id(update_order_form.customer_id.data)
        order.set_order_id(update_order_form.order_id.data)
        order.set_item_id(update_order_form.item_id.data)
        order.set_item_quantity(update_order_form.item_quantity.data)

        db['Orders'] = orders_dict
        db.close()

        return redirect(url_for('retrieve_orders'))
    else:
        orders_dict = {}
        db = shelve.open('order.db', 'r')
        orders_dict = db['Orders']
        db.close()

        order = orders_dict.get(id)
        update_order_form.customer_id.data = order.get_customer_id()
        update_order_form.order_id.data = order.get_order_id()
        update_order_form.item_id.data = order.get_item_id()
        update_order_form.item_quantity.data = order.get_item_quantity()

        return render_template('updateOrder.html', form=update_order_form)


@app.route('/deleteOrder/<id>', methods=['POST'])
def delete_order(id):
    order_dict = {}
    db = shelve.open('order.db', 'w')
    orders_dict = db['Orders']

    orders_dict.pop(id)

    db['Orders'] = orders_dict
    db.close()

    return redirect(url_for('retrieve_orders'))


@app.route('/createReport', methods=['GET', 'POST'])
def create_report():
    form = ReportForm(request.form)
    if request.method == 'POST' and form.validate():
        report_dict = {}
        db = shelve.open('report.db', 'c')

        try:
            report_dict = db['Report']
        except:
            print("Error in submiting report")

        report = Report.Report(
            form.email.data, form.issue.data, form.remarks.data)
        report_dict[report.get_report_id()] = report
        db['Report'] = report_dict

        db.close()

        return redirect(url_for('retrieve_reports'))

    return render_template('createReport.html', form=form)


@app.route('/deleteReport/<int:id>', methods=['POST'])
def delete_Report(id):
    report_dict = {}
    db = shelve.open('report.db', 'w')
    report_dict = db['Report']

    report_dict.pop(id)

    db['Report'] = report_dict
    db.close()

    return redirect(url_for('retrieve_report'))


@app.route('/retrieveReport')
def retrieve_report():
    report_dict = {}
    db = shelve.open('report.db', 'r')
    report_dict = db['Report']
    db.close()

    report_list = []
    for key in report_dict:
        report = report_dict.get(key)
        report_list.append(report)

    return render_template('retrieveReport.html', count=len(report_list), customers_list=report_list)


@app.route('/updateReport/<int:id>/', methods=['GET', 'POST'])
def update_report(id):
    Update_Report_Form = ReportForm(request.form)
    if request.method == 'POST' and Update_Report_Form.validate():
        report_dict = {}
        db = shelve.open('report.db', 'w')
        report_dict = db['Report']

        report = report_dict.get(id)
        report.set_email(Update_Report_Form.email.data)
        report.set_issue(Update_Report_Form.issue.data)
        report.set_remarks(Update_Report_Form.remarks.data)

        db['Report'] = report_dict
        db.close()

        return redirect(url_for('retrieve_report'))
    else:
        report_dict = {}
        db = shelve.open('report.db', 'r')
        report_dict = db['Report']
        db.close()

        report = report_dict.get(id)
        Update_Report_Form.email.data = report.get_email()
        Update_Report_Form.issue.data = report.get_issue()
        Update_Report_Form.remarks.data = report.get_remarks()

        return render_template('updatereport.html', form=Update_Report_Form)


if __name__ == '__main__':
    app.run()
