# jalali_shamsi_datepicker/install.py
import frappe

def post_install():
    # امن‌ترین کار این است که همین پچ را صدا بزنی (idempotent)
    try:
        frappe.get_attr("jalali_shamsi_datepicker.patches.add_yyyy_mm_dd_date_format.execute")()
    except Exception:
        frappe.log_error(frappe.get_traceback(), "jalali_shamsi_datepicker.post_install")