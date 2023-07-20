############################################
# SORTING REVIEWS
############################################

import pandas as pd
import math
import scipy.stats as st

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

###################################################
# Up-Down Diff Score = (up ratings) − (down ratings)
###################################################

# Review 1: 600 up 400 down total 1000
# Review 2: 5500 up 4500 down total 10000

def score_up_down_diff(up, down):
    return up - down

# Review 1 Score:
score_up_down_diff(600, 400)

# Review 2 Score
score_up_down_diff(5500, 4500)

###################################################
# Score = Average rating = (up ratings) / (all ratings)
###################################################

def score_average_rating(up, down):
    if up + down == 0:
        return 0
    return up / (up+down)

score_average_rating(600, 400)
score_average_rating(5500, 4500)

# Review 1: 2 up 0 down total 2
# Review 2: 100 up 1 down total 101

score_average_rating(2, 0)
score_average_rating(100, 1)

#not: bu örnekte görüyoruz ki, frekans bilgisini gözden kaçırmış olduğu için 2 yorum alanın ratingini 1 hesaplıyor ve daha çok öne çıkarıyor.

###################################################
# Wilson Lower Bound Score
###################################################

#bize ikili interaction lar barındıran herhangi bir item, product ya da review u scorlama imkanı sağlar.
#(like-dislike gibi)

#bernoulli parametresi p için bir güven aralığı hesaplar ve bu güven aralığının alt sınırını WBL score olarak kabul eder.
#not: Skorların 1-5 arasında olduğu durumlarda, skorun '0' olarak hesaplama ihtimalinin olması, Wilson Lower Bound yerine Bayesian Ortalama Hesabının tercih edilmesine sebep olur.

# 600-400
# 0.6
# 0.5 0.7
# 0.5

def wilson_lower_bound(up, down, confidence=0.95):
    """
    Wilson Lower Bound Score hesapla

    - Bernoulli parametresi p için hesaplanacak güven aralığının alt sınırı WLB skoru olarak kabul edilir.
    - Hesaplanacak skor ürün sıralaması için kullanılır.
    - Not:
    Eğer skorlar 1-5 arasıdaysa 1-3 negatif, 4-5 pozitif olarak işaretlenir ve bernoulli'ye uygun hale getirilebilir.
    Bu beraberinde bazı problemleri de getirir. Bu sebeple bayesian average rating yapmak gerekir.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


#not: aslında burada 600 veya 5500 yorumun ne kadar faydalı bulunup bulunmadığına bakıyoruz
wilson_lower_bound(600, 400)
wilson_lower_bound(5500, 4500)

wilson_lower_bound(2, 0) #bu yöntemle buradaki gerçeğe yakın durum ortaya çıkıyor aslında, skor 1 fe3n 0.34 e düştü
wilson_lower_bound(100, 1)

#sonuç: elimdeki örnekteki up rate oranının, istatistiksel olarak %95 güven ve %5 hata payı ile artık hangi aralıkta olabileceğini biliyorum.
#en alttan bir referans noktasına tutundum.

###################################################
# Case Study
###################################################

#not: çok faydalı bulunan yorumların arka sıralarda olmasının sebebi, yorum eleştiri içerdiği için baskılanmasıdır.

#soru
#Hangisi Bayesian Average Rating (BAR) ile Wilson Lower Bound (WLB) skorları arasındaki farklardan biridir?
#WLB yöntemi yalnızca pozitif yorumları dikkate alırken BAR yöntemi 'K' skalasında bütün oyları dikkate alır.




