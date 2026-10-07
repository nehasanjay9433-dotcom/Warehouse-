from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient
# ==========================================
# MONGODB CONNECTION
# ==========================================
try:
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client["warehouseDB"]
    print("MongoDB Connected Successfully!")
except Exception as e:
    print("Connection Error :", e)


# ==========================================
# MODERN CLEAN THEME SETUP
# ==========================================
def apply_modern_theme(root):
    style = ttk.Style()
    style.theme_use("clam")

    BG_DARK = "#0f172a"      # Slate 900
    PANEL_BG = "#1e293b"     # Slate 800
    ACCENT_CYAN = "#06b6d4"   # Cyan 500
    ACCENT_HOVER = "#0891b2"  # Cyan 600
    TEXT_LIGHT = "#f8fafc"    # Slate 50
    TREE_BG = "#0f172a"
    TREE_SELECT = "#334155"

    root.configure(bg=BG_DARK)

    # General TTK Styles
    style.configure("TNotebook", background=BG_DARK, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=PANEL_BG,
        foreground=TEXT_LIGHT,
        font=("Segoe UI", 10, "bold"),
        padding=[20, 10],
        borderwidth=0,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", ACCENT_CYAN)],
        foreground=[("selected", "#ffffff")],
    )

    style.configure("TFrame", background=BG_DARK)

    style.configure(
        "TLabelframe",
        background=PANEL_BG,
        foreground=ACCENT_CYAN,
        font=("Segoe UI", 11, "bold"),
        borderwidth=0,
        relief="flat",
    )
    style.configure("TLabelframe.Label", background=PANEL_BG, foreground=ACCENT_CYAN)

    style.configure(
        "TLabel", background=PANEL_BG, foreground=TEXT_LIGHT, font=("Segoe UI", 10)
    )

    style.configure(
        "Action.TButton",
        font=("Segoe UI", 10, "bold"),
        background=ACCENT_CYAN,
        foreground="#ffffff",
        borderwidth=0,
        focusthickness=0,
        padding=8,
    )
    style.map("Action.TButton", background=[("active", ACCENT_HOVER)])

    # Treeview (Tables) Styling
    style.configure(
        "Treeview",
        background=TREE_BG,
        foreground=TEXT_LIGHT,
        fieldbackground=TREE_BG,
        rowheight=30,
        font=("Segoe UI", 10),
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background=PANEL_BG,
        foreground=ACCENT_CYAN,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
    )
    style.map("Treeview", background=[("selected", TREE_SELECT)])


# ==========================================
# LOGIN WINDOW
# ==========================================
class LoginWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Inventory System - Login")
        self.root.geometry("450x340")
        self.root.resizable(False, False)
        apply_modern_theme(root)

        title = tk.Label(
            root,
            text="Warehouse System Login",
            font=("Segoe UI", 18, "bold"),
            bg="#0f172a",
            fg="#06b6d4",
        )
        title.pack(pady=30)

        frame = tk.Frame(root, bg="#1e293b", padx=25, pady=25)
        frame.pack(pady=10)

        tk.Label(
            frame,
            text="Username",
            font=("Segoe UI", 11),
            bg="#1e293b",
            fg="#f8fafc",
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username = ttk.Entry(frame, font=("Segoe UI", 11))
        self.username.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(
            frame,
            text="Password",
            font=("Segoe UI", 11),
            bg="#1e293b",
            fg="#f8fafc",
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password = ttk.Entry(frame, show="*", font=("Segoe UI", 11))
        self.password.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(root, text="LOGIN", style="Action.TButton", width=22, command=self.login).pack(pady=20)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user == "admin" and pwd == "admin123":
            messagebox.showinfo("Success", "Login Successful")
            self.root.destroy()
            main_root = tk.Tk()
            WarehouseApp(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")


# ==========================================
# MAIN DASHBOARD
# ==========================================
class WarehouseApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Inventory Dashboard")
        self.root.geometry("1150x720")
        apply_modern_theme(root)

        header = tk.Frame(root, bg="#1e293b", height=60)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="WAREHOUSE INVENTORY MANAGEMENT SYSTEM",
            font=("Segoe UI", 16, "bold"),
            bg="#1e293b",
            fg="#06b6d4",
        )
        title.pack(pady=15, padx=20, side="left")

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self.products_tab = ttk.Frame(notebook)
        self.purchase_tab = ttk.Frame(notebook)
        self.sales_tab = ttk.Frame(notebook)
        self.alert_tab = ttk.Frame(notebook)
        self.report_tab = ttk.Frame(notebook)

        notebook.add(self.products_tab, text="📦 Products")
        notebook.add(self.purchase_tab, text="📥 Purchase")
        notebook.add(self.sales_tab, text="🛒 Sales")
        notebook.add(self.alert_tab, text="⚠️ Low Stock Alerts")
        notebook.add(self.report_tab, text="📊 Analytics & Reports")

        self.setup_products_tab()
        self.setup_purchase_tab()
        self.setup_sales_tab()
        self.setup_alert_tab()
        self.setup_report_tab()

    # ------------------------------------------
    # PRODUCTS TAB
    # ------------------------------------------
    def setup_products_tab(self):
        frame = ttk.LabelFrame(self.products_tab, text=" Manage Product Catalog ", padding=15)
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Product ID").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.ent_pid = ttk.Entry(frame, width=18)
        self.ent_pid.grid(row=0, column=1)

        ttk.Label(frame, text="Product Name").grid(row=0, column=2, padx=8, sticky="w")
        self.ent_name = ttk.Entry(frame, width=22)
        self.ent_name.grid(row=0, column=3)

        ttk.Label(frame, text="Category").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.ent_category = ttk.Entry(frame, width=18)
        self.ent_category.grid(row=1, column=1)

        ttk.Label(frame, text="Price (₹)").grid(row=1, column=2, padx=8, sticky="w")
        self.ent_price = ttk.Entry(frame, width=22)
        self.ent_price.grid(row=1, column=3)

        ttk.Label(frame, text="Stock Qty").grid(row=2, column=0, padx=8, pady=8, sticky="w")
        self.ent_stock = ttk.Entry(frame, width=18)
        self.ent_stock.grid(row=2, column=1)

        ttk.Label(frame, text="Reorder Level").grid(row=2, column=2, padx=8, sticky="w")
        self.ent_reorder = ttk.Entry(frame, width=22)
        self.ent_reorder.grid(row=2, column=3)

        ttk.Label(frame, text="Supplier").grid(row=3, column=0, padx=8, pady=8, sticky="w")
        self.ent_supplier = ttk.Entry(frame, width=18)
        self.ent_supplier.grid(row=3, column=1)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=15)

        ttk.Button(btn_frame, text="Add Product", style="Action.TButton", command=self.add_product).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Update", style="Action.TButton", command=self.update_product).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Delete", style="Action.TButton", command=self.delete_product).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Search ID", style="Action.TButton", command=self.search_product).pack(side="left", padx=8)

        cols = ("ID", "Name", "Category", "Price", "Stock", "Reorder", "Supplier")
        self.tree = ttk.Treeview(self.products_tab, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.fill_entries_from_selection)
        self.load_products()

    def fill_entries_from_selection(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_fields()
            self.ent_pid.insert(0, values[0])
            self.ent_name.insert(0, values[1])
            self.ent_category.insert(0, values[2])
            clean_price = str(values[3]).replace("₹", "").replace(",", "").strip()
            self.ent_price.insert(0, clean_price)
            self.ent_stock.insert(0, values[4])
            self.ent_reorder.insert(0, values[5])
            self.ent_supplier.insert(0, values[6])

    def add_product(self):
        pid_str = self.ent_pid.get().strip()
        name = self.ent_name.get().strip()
        price_str = self.ent_price.get().strip()
        stock_str = self.ent_stock.get().strip()
        reorder_str = self.ent_reorder.get().strip()

        if not (pid_str and name and price_str and stock_str and reorder_str):
            messagebox.showwarning("Input Missing", "Please fill in all required fields!")
            return

        try:
            pid = int(pid_str)
            price = float(price_str)
            stock = int(stock_str)
            reorder = int(reorder_str)

            if db.products.find_one({"product_id": pid}):
                messagebox.showerror("Duplicate ID", f"Product ID {pid} already exists!")
                return

            data = {
                "product_id": pid,
                "name": name,
                "category": self.ent_category.get().strip(),
                "unit_price": price,
                "stock_qty": stock,
                "reorder_level": reorder,
                "supplier_name": self.ent_supplier.get().strip(),
            }
            db.products.insert_one(data)
            messagebox.showinfo("Success", "Product Added Successfully!")
            self.clear_fields()
            self.load_products()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for ID, Price, Stock, and Reorder Level!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_products(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in db.products.find():
            self.tree.insert(
                "",
                tk.END,
                values=(
                    p.get("product_id"),
                    p.get("name"),
                    p.get("category"),
                    f"₹{p.get('unit_price', 0):,.2f}",
                    p.get("stock_qty"),
                    p.get("reorder_level"),
                    p.get("supplier_name"),
                ),
            )

    def update_product(self):
        pid_str = self.ent_pid.get().strip()
        if not pid_str:
            messagebox.showwarning("Input Missing", "Please enter Product ID to update!")
            return

        try:
            pid = int(pid_str)
            db.products.update_one(
                {"product_id": pid},
                {
                    "$set": {
                        "name": self.ent_name.get().strip(),
                        "category": self.ent_category.get().strip(),
                        "unit_price": float(self.ent_price.get().strip()),
                        "stock_qty": int(self.ent_stock.get().strip()),
                        "reorder_level": int(self.ent_reorder.get().strip()),
                        "supplier_name": self.ent_supplier.get().strip(),
                    }
                },
            )
            messagebox.showinfo("Updated", "Product Updated Successfully!")
            self.clear_fields()
            self.load_products()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for Price, Stock, and Reorder Level!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_product(self):
        pid_str = self.ent_pid.get().strip()
        if not pid_str:
            messagebox.showwarning("Input Missing", "Please enter Product ID to delete!")
            return

        try:
            pid = int(pid_str)
            res = db.products.delete_one({"product_id": pid})
            if res.deleted_count > 0:
                messagebox.showinfo("Deleted", f"Product ID {pid} deleted successfully!")
                self.clear_fields()
                self.load_products()
            else:
                messagebox.showerror("Not Found", f"Product ID {pid} not found!")
        except ValueError:
            messagebox.showerror("Invalid Input", "Product ID must be numeric!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_product(self):
        pid_str = self.ent_pid.get().strip()
        if not pid_str:
            messagebox.showwarning("Input Missing", "Please enter Product ID to search!")
            return

        try:
            pid = int(pid_str)
            p = db.products.find_one({"product_id": pid})
            if p:
                messagebox.showinfo(
                    "Product Found", f"Name: {p.get('name')}\nCategory: {p.get('category')}\nStock: {p.get('stock_qty')}\nPrice: ₹{p.get('unit_price')}"
                )
            else:
                messagebox.showerror("Not Found", f"Product ID {pid} not found!")
        except ValueError:
            messagebox.showerror("Invalid Input", "Product ID must be numeric!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_fields(self):
        self.ent_pid.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_category.delete(0, tk.END)
        self.ent_price.delete(0, tk.END)
        self.ent_stock.delete(0, tk.END)
        self.ent_reorder.delete(0, tk.END)
        self.ent_supplier.delete(0, tk.END)

    # ------------------------------------------
    # PURCHASE TAB
    # ------------------------------------------
    def setup_purchase_tab(self):
        top_frame = ttk.Frame(self.purchase_tab)
        top_frame.pack(fill="x", padx=10, pady=10)

        frame = ttk.LabelFrame(top_frame, text=" Record Stock Purchase ", padding=15)
        frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        ttk.Label(frame, text="Product ID").grid(row=0, column=0, padx=8, pady=5, sticky="w")
        self.p_pid = ttk.Entry(frame, width=20)
        self.p_pid.grid(row=0, column=1)

        ttk.Label(frame, text="Quantity").grid(row=1, column=0, padx=8, pady=5, sticky="w")
        self.p_qty = ttk.Entry(frame, width=20)
        self.p_qty.grid(row=1, column=1)

        ttk.Label(frame, text="Supplier").grid(row=2, column=0, padx=8, pady=5, sticky="w")
        self.p_supplier = ttk.Entry(frame, width=20)
        self.p_supplier.grid(row=2, column=1)

        ttk.Label(frame, text="Unit Cost (₹)").grid(row=3, column=0, padx=8, pady=5, sticky="w")
        self.p_cost = ttk.Entry(frame, width=20)
        self.p_cost.grid(row=3, column=1)

        ttk.Button(
            frame, text="Record Purchase", style="Action.TButton", command=self.record_purchase
        ).grid(row=4, column=0, columnspan=2, pady=10)

        # Purchase Records Treeview Table
        table_frame = ttk.LabelFrame(self.purchase_tab, text=" Purchase History ", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        p_cols = ("Product ID", "Supplier", "Quantity", "Unit Cost", "Total Amount", "Date")
        self.p_tree = ttk.Treeview(table_frame, columns=p_cols, show="headings")

        for col in p_cols:
            self.p_tree.heading(col, text=col)
            self.p_tree.column(col, width=140, anchor="center")

        self.p_tree.pack(fill="both", expand=True)
        self.load_purchases()

    def record_purchase(self):
        try:
            pid = int(self.p_pid.get().strip())
            qty = int(self.p_qty.get().strip())
            supplier = self.p_supplier.get().strip()
            cost = float(self.p_cost.get().strip())

            db.purchase.insert_one(
                {
                    "product_id": pid,
                    "supplier_name": supplier,
                    "qty": qty,
                    "unit_cost": cost,
                    "purchase_date": datetime.now(),
                }
            )

            db.products.update_one({"product_id": pid}, {"$inc": {"stock_qty": qty}})
            messagebox.showinfo("Success", "Purchase Recorded Successfully")
            
            # Clear Inputs
            self.p_pid.delete(0, tk.END)
            self.p_qty.delete(0, tk.END)
            self.p_supplier.delete(0, tk.END)
            self.p_cost.delete(0, tk.END)

            self.load_products()
            self.load_purchases()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_purchases(self):
        for item in self.p_tree.get_children():
            self.p_tree.delete(item)

        purchases = db.purchase.find().sort("purchase_date", -1)
        for p in purchases:
            p_date = p.get("purchase_date")
            date_str = p_date.strftime("%Y-%m-%d %H:%M:%S") if isinstance(p_date, datetime) else "N/A"
            total = p.get("qty", 0) * p.get("unit_cost", 0)

            self.p_tree.insert(
                "",
                tk.END,
                values=(
                    p.get("product_id"),
                    p.get("supplier_name", "N/A"),
                    p.get("qty"),
                    f"₹{p.get('unit_cost', 0):,.2f}",
                    f"₹{total:,.2f}",
                    date_str,
                ),
            )

    # ------------------------------------------
    # SALES TAB
    # ------------------------------------------
    def setup_sales_tab(self):
        top_frame = ttk.Frame(self.sales_tab)
        top_frame.pack(fill="x", padx=10, pady=10)

        frame = ttk.LabelFrame(top_frame, text=" Record New Sale ", padding=15)
        frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        ttk.Label(frame, text="Customer").grid(row=0, column=0, padx=8, pady=5, sticky="w")
        self.s_customer = ttk.Entry(frame, width=20)
        self.s_customer.grid(row=0, column=1)

        ttk.Label(frame, text="Product ID").grid(row=1, column=0, padx=8, pady=5, sticky="w")
        self.s_pid = ttk.Entry(frame, width=20)
        self.s_pid.grid(row=1, column=1)

        ttk.Label(frame, text="Quantity").grid(row=2, column=0, padx=8, pady=5, sticky="w")
        self.s_qty = ttk.Entry(frame, width=20)
        self.s_qty.grid(row=2, column=1)

        ttk.Label(frame, text="Unit Price (₹)").grid(row=3, column=0, padx=8, pady=5, sticky="w")
        self.s_price = ttk.Entry(frame, width=20)
        self.s_price.grid(row=3, column=1)

        ttk.Button(frame, text="Process Sale", style="Action.TButton", command=self.record_sale).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        # Sales Records Treeview Table
        table_frame = ttk.LabelFrame(self.sales_tab, text=" Sales History ", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        s_cols = ("Customer", "Product ID", "Quantity", "Unit Price", "Total Amount", "Date")
        self.s_tree = ttk.Treeview(table_frame, columns=s_cols, show="headings")

        for col in s_cols:
            self.s_tree.heading(col, text=col)
            self.s_tree.column(col, width=140, anchor="center")

        self.s_tree.pack(fill="both", expand=True)
        self.load_sales()

    def record_sale(self):
        try:
            pid = int(self.s_pid.get().strip())
            qty = int(self.s_qty.get().strip())
            customer = self.s_customer.get().strip()
            price = float(self.s_price.get().strip())

            product = db.products.find_one({"product_id": pid})

            if not product:
                messagebox.showerror("Error", "Product Not Found")
                return

            if product["stock_qty"] < qty:
                messagebox.showerror("Error", "Insufficient Stock")
                return

            db.sales.insert_one(
                {
                    "customer_name": customer,
                    "product_id": pid,
                    "qty": qty,
                    "unit_price": price,
                    "sale_date": datetime.now(),
                }
            )

            updated_product = db.products.find_one_and_update(
                {"product_id": pid},
                {"$inc": {"stock_qty": -qty}},
                return_document=True,
            )

            if updated_product["stock_qty"] <= updated_product["reorder_level"]:
                db.alerts.insert_one(
                    {
                        "product_id": pid,
                        "current_qty": updated_product["stock_qty"],
                        "alert_date": datetime.now(),
                    }
                )

            messagebox.showinfo("Success", "Sale Recorded Successfully")

            # Clear Inputs
            self.s_customer.delete(0, tk.END)
            self.s_pid.delete(0, tk.END)
            self.s_qty.delete(0, tk.END)
            self.s_price.delete(0, tk.END)

            self.load_products()
            self.load_sales()
            self.load_alerts()
            self.generate_report()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_sales(self):
        for item in self.s_tree.get_children():
            self.s_tree.delete(item)

        sales = db.sales.find().sort("sale_date", -1)
        for s in sales:
            s_date = s.get("sale_date")
            date_str = s_date.strftime("%Y-%m-%d %H:%M:%S") if isinstance(s_date, datetime) else "N/A"
            total = s.get("qty", 0) * s.get("unit_price", 0)

            self.s_tree.insert(
                "",
                tk.END,
                values=(
                    s.get("customer_name", "N/A"),
                    s.get("product_id"),
                    s.get("qty"),
                    f"₹{s.get('unit_price', 0):,.2f}",
                    f"₹{total:,.2f}",
                    date_str,
                ),
            )

    # ------------------------------------------
    # ALERTS TAB
    # ------------------------------------------
    def setup_alert_tab(self):
        columns = ("Product ID", "Current Stock", "Alert Date")
        self.alert_tree = ttk.Treeview(
            self.alert_tab, columns=columns, show="headings"
        )

        for col in columns:
            self.alert_tree.heading(col, text=col)
            self.alert_tree.column(col, width=250, anchor="center")

        self.alert_tree.pack(fill="both", expand=True, padx=15, pady=15)

        ttk.Button(
            self.alert_tab, text="Refresh Alerts List", style="Action.TButton", command=self.load_alerts
        ).pack(pady=10)
        self.load_alerts()

    def load_alerts(self):
        for item in self.alert_tree.get_children():
            self.alert_tree.delete(item)

        alerts = db.alerts.find().sort("alert_date", -1)

        for alert in alerts:
            alert_date = alert.get("alert_date")
            date_str = (
                alert_date.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(alert_date, datetime)
                else "N/A"
            )
            self.alert_tree.insert(
                "",
                tk.END,
                values=(
                    alert.get("product_id"),
                    alert.get("current_qty"),
                    date_str,
                ),
            )

    # ------------------------------------------
    # ADVANCED REPORTS & ANALYTICS TAB
    # ------------------------------------------
    def setup_report_tab(self):
        top_bar = ttk.Frame(self.report_tab)
        top_bar.pack(fill="x", padx=15, pady=10)

        ttk.Button(
            top_bar, text="🔄 Refresh Analytics", style="Action.TButton", command=self.generate_report
        ).pack(side="left", padx=5)

        ttk.Button(
            top_bar, text="💾 Export Summary to Text", style="Action.TButton", command=self.export_report
        ).pack(side="left", padx=5)

        cards_frame = ttk.Frame(self.report_tab)
        cards_frame.pack(fill="x", padx=15, pady=5)

        # Card 1: Total Inventory Value (Cyan)
        card1 = tk.Frame(cards_frame, bg="#0284c7", padx=20, pady=15)
        card1.grid(row=0, column=0, padx=8, pady=5, sticky="nsew")
        tk.Label(card1, text="TOTAL INVENTORY VALUE", font=("Segoe UI", 9, "bold"), bg="#0284c7", fg="#e0f2fe").pack(anchor="w")
        self.lbl_total = tk.Label(card1, text="₹0.00", font=("Segoe UI", 18, "bold"), bg="#0284c7", fg="#ffffff")
        self.lbl_total.pack(anchor="w", pady=(5, 0))

        # Card 2: Total Products (Purple)
        card2 = tk.Frame(cards_frame, bg="#7c3aed", padx=20, pady=15)
        card2.grid(row=0, column=1, padx=8, pady=5, sticky="nsew")
        tk.Label(card2, text="TOTAL PRODUCTS", font=("Segoe UI", 9, "bold"), bg="#7c3aed", fg="#f3e8ff").pack(anchor="w")
        self.lbl_count = tk.Label(card2, text="0", font=("Segoe UI", 18, "bold"), bg="#7c3aed", fg="#ffffff")
        self.lbl_count.pack(anchor="w", pady=(5, 0))

        # Card 3: Low Stock Alerts (Red)
        card3 = tk.Frame(cards_frame, bg="#dc2626", padx=20, pady=15)
        card3.grid(row=0, column=2, padx=8, pady=5, sticky="nsew")
        tk.Label(card3, text="LOW STOCK ALERTS", font=("Segoe UI", 9, "bold"), bg="#dc2626", fg="#fee2e2").pack(anchor="w")
        self.lbl_alerts = tk.Label(card3, text="0", font=("Segoe UI", 18, "bold"), bg="#dc2626", fg="#ffffff")
        self.lbl_alerts.pack(anchor="w", pady=(5, 0))

        # Card 4: Total Revenue Generated (Green)
        card4 = tk.Frame(cards_frame, bg="#059669", padx=20, pady=15)
        card4.grid(row=0, column=3, padx=8, pady=5, sticky="nsew")
        tk.Label(card4, text="TOTAL SALES REVENUE", font=("Segoe UI", 9, "bold"), bg="#059669", fg="#d1fae5").pack(anchor="w")
        self.lbl_sales = tk.Label(card4, text="₹0.00", font=("Segoe UI", 18, "bold"), bg="#059669", fg="#ffffff")
        self.lbl_sales.pack(anchor="w", pady=(5, 0))

        for i in range(4):
            cards_frame.columnconfigure(i, weight=1)

        tables_frame = ttk.Frame(self.report_tab)
        tables_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Left Table: Category Breakdown
        cat_frame = ttk.LabelFrame(tables_frame, text=" Category-wise Stock Summary ", padding=10)
        cat_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        cols_cat = ("Category", "Products", "Total Value")
        self.tree_cat = ttk.Treeview(cat_frame, columns=cols_cat, show="headings", height=8)
        for c in cols_cat:
            self.tree_cat.heading(c, text=c)
            self.tree_cat.column(c, width=120, anchor="center")
        self.tree_cat.pack(fill="both", expand=True)

        # Right Table: Recent Sales Activity
        sales_frame = ttk.LabelFrame(tables_frame, text=" Recent Sales Transactions ", padding=10)
        sales_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))

        cols_sales = ("Customer", "Prod ID", "Qty", "Amount")
        self.tree_recent_sales = ttk.Treeview(sales_frame, columns=cols_sales, show="headings", height=8)
        for c in cols_sales:
            self.tree_recent_sales.heading(c, text=c)
            self.tree_recent_sales.column(c, width=100, anchor="center")
        self.tree_recent_sales.pack(fill="both", expand=True)

        self.generate_report()

    def generate_report(self):
        pipeline_inv = [
            {"$project": {"total": {"$multiply": ["$stock_qty", "$unit_price"]}}},
            {"$group": {"_id": None, "InventoryValue": {"$sum": "$total"}}},
        ]
        res_inv = list(db.products.aggregate(pipeline_inv))
        total_inv = res_inv[0]["InventoryValue"] if res_inv else 0

        count_products = db.products.count_documents({})
        count_alerts = db.alerts.count_documents({})

        pipeline_sales = [
            {"$project": {"total": {"$multiply": ["$qty", "$unit_price"]}}},
            {"$group": {"_id": None, "SalesValue": {"$sum": "$total"}}},
        ]
        res_sales = list(db.sales.aggregate(pipeline_sales))
        total_sales = res_sales[0]["SalesValue"] if res_sales else 0

        self.lbl_total.config(text=f"₹{total_inv:,.2f}")
        self.lbl_count.config(text=str(count_products))
        self.lbl_alerts.config(text=str(count_alerts))
        self.lbl_sales.config(text=f"₹{total_sales:,.2f}")

        for row in self.tree_cat.get_children():
            self.tree_cat.delete(row)

        pipeline_cat = [
            {
                "$group": {
                    "_id": "$category",
                    "count": {"$sum": 1},
                    "total_val": {"$sum": {"$multiply": ["$stock_qty", "$unit_price"]}},
                }
            }
        ]
        cat_data = list(db.products.aggregate(pipeline_cat))
        for item in cat_data:
            cat_name = item["_id"] if item["_id"] else "Uncategorized"
            self.tree_cat.insert("", tk.END, values=(cat_name, item["count"], f"₹{item['total_val']:,.2f}"))

        for row in self.tree_recent_sales.get_children():
            self.tree_recent_sales.delete(row)

        recent_sales = db.sales.find().sort("sale_date", -1).limit(10)
        for s in recent_sales:
            amount = s.get("qty", 0) * s.get("unit_price", 0)
            self.tree_recent_sales.insert(
                "",
                tk.END,
                values=(
                    s.get("customer_name", "N/A"),
                    s.get("product_id"),
                    s.get("qty"),
                    f"₹{amount:,.2f}",
                ),
            )

    def export_report(self):
        try:
            filename = f"Inventory_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("==============================================\n")
                f.write("      WAREHOUSE INVENTORY ANALYTICS REPORT    \n")
                f.write(f"      Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("==============================================\n\n")
                f.write(f"Total Inventory Value : {self.lbl_total.cget('text')}\n")
                f.write(f"Total Product Count   : {self.lbl_count.cget('text')}\n")
                f.write(f"Low Stock Alerts      : {self.lbl_alerts.cget('text')}\n")
                f.write(f"Total Revenue Sales   : {self.lbl_sales.cget('text')}\n")
                f.write("\n==============================================\n")

            messagebox.showinfo("Exported", f"Summary successfully saved to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))


# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    login_root = tk.Tk()
    app = LoginWindow(login_root)
    login_root.mainloop()

