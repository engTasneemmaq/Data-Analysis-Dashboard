from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load data
data_file = 'data.csv'
df = pd.read_csv(data_file)

@app.route('/')
def dashboard():
    # Get filter criteria from request
    product_filter = request.args.get('product', 'all')

    # Filter data
    if product_filter != 'all':
        filtered_df = df[df['Product'] == product_filter]
    else:
        filtered_df = df

    # Recalculate summary and plot
    total_sales = (filtered_df['Quantity'] * filtered_df['Price']).sum()
    total_products_sold = filtered_df['Quantity'].sum()
    unique_products = filtered_df['Product'].nunique()
    unique_products_list = df['Product'].unique()

    # Generate plot
    sales_by_product = filtered_df.groupby('Product')['Quantity'].sum()
    plt.figure(figsize=(8, 5))
    sales_by_product.plot(kind='bar', color='skyblue')
    plt.title('Sales by Product')
    plt.xlabel('Product')
    plt.ylabel('Quantity Sold')
    plt.tight_layout()
    plt.savefig('static/sales_plot.png')
    plt.close()

    return render_template(
        'dashboard.html',
        total_sales=total_sales,
        total_products_sold=total_products_sold,
        unique_products=unique_products,
        unique_products_list=unique_products_list,
        plot_url='/static/sales_plot.png'
    )

if __name__ == '__main__':
    app.run(debug=True)
