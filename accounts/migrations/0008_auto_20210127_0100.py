# Generated by Django 3.1.1 on 2021-01-26 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210127_0058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actionlogs',
            old_name='remote_id',
            new_name='remote_ip',
        ),
        migrations.AlterField(
            model_name='game',
            name='category',
            field=models.CharField(blank=True, choices=[('Casino', 'Casino'), ('Fish', 'Fish'), ('7/11', '7/11'), ('Sports', 'Sports'), ('Slot', 'Slot')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='game_category',
            field=models.CharField(blank=True, choices=[('Casino', 'Casino'), ('Fish', 'Fish'), ('7/11', '7/11'), ('Sports', 'Sports'), ('Slot', 'Slot')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='restriction_category',
            field=models.CharField(blank=True, choices=[('Casino', 'Casino'), ('Fish', 'Fish'), ('7/11', '7/11'), ('Sports', 'Sports'), ('Slot', 'Slot')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='tag1',
            field=models.CharField(blank=True, choices=[('Promo', 'Promo'), ('Recommend', 'Recommend'), ('Void Credit', 'Void Credit'), ('Lock Credit', 'Lock Credit'), ('Borrow Credit', 'Borrow Credit'), ('Withdrawal', 'Withdrawal'), ('Free Credit', 'Free Credit')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='tag2',
            field=models.CharField(blank=True, choices=[('Ticket', 'Ticket'), ('No Bonus', 'No Bonus'), ('No Bonus Topup', 'No Bonus (Below Minimum Topup Amount)'), ('Rebate Bonus', 'Rebate Bonus')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='usage',
            field=models.CharField(blank=True, choices=[('Thrice a Day', 'Thrice a Day'), ('Yearly', 'Yearly'), ('Daily', 'Daily'), ('One Time Only', 'One Time Only'), ('Monthly', 'Monthly'), ('Unlimited', 'Unlimited'), ('Weekly', 'Weekly'), ('Twice a Day', 'Twice a Day')], max_length=200, null=True),
        ),
    ]