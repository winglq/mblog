from mblog.db.models import Stock
from mblog.db.models import get_session


def stock_create(user, code, hold_position, bid_price,
                 stop_loss_price, selled=False,
                 sell_price=None):
    s = Stock(user=user, code=code, hold_position=hold_position,
              bid_price=bid_price, stop_loss_price=stop_loss_price,
              selled=selled, sell_price=sell_price)
    sess = get_session()
    sess.add(s)
    sess.commit()


def stock_list(user):
    sess = get_session()
    return sess.query(Stock).filter_by(user=user)


def stock_delete(sid):
    sess = get_session()
    stock = sess.query(Stock).get(sid)
    sess.delete(stock)
    sess.commit()


#def stock_update(id, hold_position=None, bid_price=None, stop_loss_price=None,
#                 selled=None, sell_price=None):
def stock_update(sid, **kwargs):
    sess = get_session()
    stock = sess.query(Stock).filter_by(id=sid).update(kwargs)
    sess.commit()
