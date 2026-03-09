from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_review_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images/')),
                ('is_primary', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='SpecialPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='special_price', to='products.product')),
            ],
        ),
    ]
