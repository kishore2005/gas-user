import flet as ft
import sqlitecloud

def fetch_products():
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gas?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('SELECT id, image, name, price FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

def book_product(user_id, product_id):
    conn = sqlitecloud.connect("sqlitecloud://ce3yvllesk.sqlite.cloud:8860/gas?apikey=kOt8yvfwRbBFka2FXT1Q1ybJKaDEtzTya3SWEGzFbvE")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO bookings (user_id, product_id) VALUES (?, ?)', (user_id, product_id))
    conn.commit()
    conn.close()

def show_products(page: ft.Page, user):
    # Fetch products from the database
    products = fetch_products()

    # Create a list to hold product containers
    product_containers = []

    for product in products:
        product_id, product_image_url, product_name, product_price = product

        def on_book(e):
            book_product(user[0], product_id)
            page.snack_bar = ft.SnackBar(ft.Text(f"Product {product_name} booked successfully!"), open=True)

        # Create a container to add padding around the card
        product_container = ft.Container(
            content=ft.Card(
                content=ft.Column(
                    [
                        ft.Image(src=product_image_url, width=300, height=300),  # Adjusted image size
                        ft.Text(product_name, size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),  # Adjusted text size and alignment
                        ft.Text(f"₹{product_price}", size=25, color=ft.colors.GREEN, text_align=ft.TextAlign.CENTER),  # Adjusted text size and alignment
                        ft.ElevatedButton(text="Book Now", on_click=on_book)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                elevation=5,
            ),
            padding=30,
            alignment=ft.alignment.center  # Center the container content
        )

        # Add the product container to the list
        product_containers.append(product_container)

    # Create a scrollable column to hold all product containers
    scrollable_column = ft.Column(
        controls=product_containers,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
    )

    # Add the scrollable column to the page
    page.add(scrollable_column)
