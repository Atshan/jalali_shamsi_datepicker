# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

def execute():
    """
    Add 'yyyy/mm/dd' option to the 'date_format' field of System Settings
    in an idempotent way.
    """
    doctype = "System Settings"
    fieldname = "date_format"  # نام فیلد در DocType
    # مقدار پیشنهادی که می‌خواهیم اضافه کنیم (مطابق نیازی که گفتید)
    new_option = "yyyy/mm/dd"

    try:
        dt = frappe.get_meta(doctype)
        field = None
        for f in dt.fields:
            if f.fieldname == fieldname:
                field = f
                break

        if not field:
            frappe.log_error(
                "jalali_shamsi_datepicker: could not find field {} in {}".format(fieldname, doctype),
                "add_yyyy_mm_dd_date_format"
            )
            return

        # فهرست گزینه‌ها را می‌گیریم و مطمئن می‌شویم که اگر از قبل هست، دوباره اضافه نشود
        options = field.options or ""
        # options ممکن است به‌صورت سطر به سطر باشد؛ آن را به لیست تبدیل می‌کنیم
        opts = [o.strip() for o in options.split("\n") if o.strip()]
        if new_option in opts:
            # از قبل اضافه شده؛ کاری انجام نمی‌دهیم
            return

        # اضافه کردن به انتهای لیست (یا می‌توانید جای دیگری insert کنید)
        opts.append(new_option)
        new_options = "\n".join(opts)

        # به‌روزرسانی فیلد در متا و ذخیره تغییر در دیتابیس DocType
        # این روش از frappe.db.sql مستقیم استفاده نمی‌کند و از API DocType بهره می‌برد
        frappe.db.sql(
            """
            UPDATE `tabDocField`
            SET `options` = %s
            WHERE `parent` = %s AND `fieldname` = %s
            """,
            (new_options, doctype, fieldname)
        )
        # clear cache so change is visible immediately
        frappe.clear_cache(doctype=doctype)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "jalali_shamsi_datepicker.add_yyyy_mm_dd_date_format")
        raise