from django.contrib import admin
from newMatrix.models import newMatrix_smallDesk, newMatix_largeDesk, newMatrix_freePlaceSmallDesk, newMatrix_UserDesk, \
    newMatrix_UserLargeDesk, newMatrix_LargeDeskSmallDesk, MatrixMoneyPay
# Register your models here.


admin.site.register(newMatrix_smallDesk)
admin.site.register(newMatix_largeDesk)
admin.site.register(newMatrix_freePlaceSmallDesk)
admin.site.register(newMatrix_UserDesk)
admin.site.register(newMatrix_UserLargeDesk)
admin.site.register(newMatrix_LargeDeskSmallDesk)
admin.site.register(MatrixMoneyPay)



