# Generated by Django 2.1.4 on 2018-12-29 04:33

from decimal import Decimal
from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_measurement.models
import django_prices.models
import saleor.core.utils.json_serializer
import saleor.core.utils.taxes
import saleor.core.weight


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shipping', '__first__'),
        ('account', '0001_initial'),
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fulfillment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fulfillment_order', models.PositiveIntegerField(editable=False)),
                ('status', models.CharField(choices=[('fulfilled', 'Fulfilled'), ('canceled', 'Canceled')], default='fulfilled', max_length=32)),
                ('tracking_number', models.CharField(blank=True, default='', max_length=255)),
                ('shipping_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='FulfillmentLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('fulfillment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='order.Fulfillment')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('unfulfilled', 'Unfulfilled'), ('partially fulfilled', 'Partially fulfilled'), ('fulfilled', 'Fulfilled'), ('canceled', 'Canceled')], default='unfulfilled', max_length=32)),
                ('language_code', models.CharField(default='en', max_length=35)),
                ('tracking_client_id', models.CharField(blank=True, editable=False, max_length=36)),
                ('user_email', models.EmailField(blank=True, default='', max_length=254)),
                ('shipping_price_net', django_prices.models.MoneyField(currency='INR', decimal_places=2, default=0, editable=False, max_digits=12)),
                ('shipping_price_gross', django_prices.models.MoneyField(currency='INR', decimal_places=2, default=0, editable=False, max_digits=12)),
                ('shipping_method_name', models.CharField(blank=True, default=None, editable=False, max_length=255, null=True)),
                ('token', models.CharField(blank=True, max_length=36, unique=True)),
                ('total_net', django_prices.models.MoneyField(currency='INR', decimal_places=2, default=saleor.core.utils.taxes.zero_money, max_digits=12)),
                ('total_gross', django_prices.models.MoneyField(currency='INR', decimal_places=2, default=saleor.core.utils.taxes.zero_money, max_digits=12)),
                ('discount_amount', django_prices.models.MoneyField(currency='INR', decimal_places=2, default=saleor.core.utils.taxes.zero_money, max_digits=12)),
                ('discount_name', models.CharField(blank=True, default='', max_length=255)),
                ('translated_discount_name', models.CharField(blank=True, default='', max_length=255)),
                ('display_gross_prices', models.BooleanField(default=True)),
                ('customer_note', models.TextField(blank=True, default='')),
                ('weight', django_measurement.models.MeasurementField(default=saleor.core.weight.zero_weight, measurement_class='Mass')),
                ('billing_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address')),
                ('shipping_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='account.Address')),
                ('shipping_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='shipping.ShippingMethod')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('voucher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='discount.Voucher')),
            ],
            options={
                'ordering': ('-pk',),
                'permissions': (('manage_orders', 'Manage orders.'),),
            },
        ),
        migrations.CreateModel(
            name='OrderEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('type', models.CharField(choices=[('PLACED', 'placed'), ('PLACED_FROM_DRAFT', 'draft_placed'), ('OVERSOLD_ITEMS', 'oversold_items'), ('ORDER_MARKED_AS_PAID', 'marked_as_paid'), ('CANCELED', 'canceled'), ('ORDER_FULLY_PAID', 'order_paid'), ('UPDATED', 'updated'), ('EMAIL_SENT', 'email_sent'), ('PAYMENT_CAPTURED', 'captured'), ('PAYMENT_REFUNDED', 'refunded'), ('PAYMENT_VOIDED', 'voided'), ('FULFILLMENT_CANCELED', 'fulfillment_canceled'), ('FULFILLMENT_RESTOCKED_ITEMS', 'restocked_items'), ('FULFILLMENT_FULFILLED_ITEMS', 'fulfilled_items'), ('TRACKING_UPDATED', 'tracking_updated'), ('NOTE_ADDED', 'note_added'), ('OTHER', 'other')], max_length=255)),
                ('parameters', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='order.Order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=386)),
                ('translated_product_name', models.CharField(blank=True, default='', max_length=386)),
                ('product_sku', models.CharField(max_length=32)),
                ('is_shipping_required', models.BooleanField()),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('quantity_fulfilled', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('unit_price_net', django_prices.models.MoneyField(currency='INR', decimal_places=2, max_digits=12)),
                ('unit_price_gross', django_prices.models.MoneyField(currency='INR', decimal_places=2, max_digits=12)),
                ('tax_rate', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=5)),
                ('order', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='order.Order')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_lines', to='product.ProductVariant')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.AddField(
            model_name='fulfillmentline',
            name='order_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='order.OrderLine'),
        ),
        migrations.AddField(
            model_name='fulfillment',
            name='order',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='fulfillments', to='order.Order'),
        ),
    ]
