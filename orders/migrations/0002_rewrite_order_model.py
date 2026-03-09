# Migration: Complete rewrite of Order model, new OrderItem, updated Address
# Replaces 0002_update_order_orderitem.py — rename that file if running fresh

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('accounts', '0002_add_face_data'),
        ('products', '0001_initial'),
    ]

    operations = [
        # Drop old Order (had product FK)
        migrations.DeleteModel(name='Order'),

        # Add new fields to Address
        migrations.AddField(
            model_name='address',
            name='full_name',
            field=models.CharField(max_length=150, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=15, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(max_length=100, default='India'),
        ),

        # Create new Order
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('pending','Pending'),('confirmed','Confirmed'),
                             ('shipped','Shipped'),('delivered','Delivered'),('cancelled','Cancelled')],
                    default='pending', max_length=20)),
                ('payment_method', models.CharField(
                    choices=[('cod','Cash on Delivery'),('online','Online Payment')],
                    default='cod', max_length=20)),
                ('payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('discount_code', models.CharField(blank=True, max_length=50, null=True)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shipping', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='orders', to='accounts.customer')),
                ('address', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                    to='orders.address')),
            ],
            options={'verbose_name': 'Order', 'ordering': ['-created_at']},
        ),

        # Create OrderItem
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items', to='orders.order')),
                ('product', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                    related_name='order_items', to='products.product')),
            ],
            options={'verbose_name': 'Order Item'},
        ),
    ]
