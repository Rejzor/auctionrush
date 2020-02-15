from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime, timezone
from math import ceil
import pytz


class Auction(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    desc = models.CharField(max_length=2000, blank=True)
    image = models.ImageField(upload_to='auction_images/', blank=True, default='auction_images/rick.jpeg')
    min_value = models.IntegerField()
    date_added = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET("(deleted)"),
                               blank=True,
                               null=True,
                               related_name="auction_winner",
                               related_query_name="auction_winner")
    final_value = models.IntegerField(blank=True, null=True)
    bid_value = models.IntegerField(blank=True, null=True)
    deadline_date = models.CharField(max_length=300)

    def convert_date_to_minutes(self):
        converted = datetime.strptime(self.deadline_date, '%d/%m/%Y %H:%M').replace(tzinfo=pytz.timezone('Europe/Warsaw'))
        return converted

    def resolve(self):
        if self.is_active:
            if self.has_expired():
                self.is_active = False
                self.save()

    # Helper function that determines if the auction has expired
    def has_expired(self):
        now = datetime.now().replace(tzinfo=pytz.timezone('Europe/Warsaw'))
        expiration = self.convert_date_to_minutes()
        if now > expiration:
            return True
        else:
            return False

    # Returns the ceiling of remaining_time in minutes
    @property
    def remaining_minutes(self):
        if self.is_active:
            now = datetime.now().replace(tzinfo=pytz.timezone('Europe/Warsaw'))
            expiration = self.convert_date_to_minutes()
            minutes_remaining = ceil((expiration - now).total_seconds() / 60)
            return(minutes_remaining)
        else:
            return(0)


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField('when the bid was made')

    def check_amount(self, bid_amount, bid_value, min_value):
        substract = int(bid_amount) - int(min_value)
        modulo = int(substract) % int(bid_value)
        if not modulo:
            return int(bid_amount)
        else:
            raise(KeyError)