import React, { useState } from "react";
import {
  ShoppingBag,
  User,
  CreditCard,
  Bell,
  Star,
  Activity,
  Package
} from "lucide-react";

const API_BASE = "";

function App() {
  const [products, setProducts] = useState([]);
  const [output, setOutput] = useState("Click a button to test the cosmetics store microservices.");
  const [loading, setLoading] = useState(false);

  const showResult = (title, data) => {
    setOutput(`${title}\n\n${JSON.stringify(data, null, 2)}`);
  };

  const handleError = (title, error) => {
    setOutput(`${title}\n\nError: ${error.message}`);
  };

  const loadProducts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/products`);
      const data = await response.json();
      setProducts(data.products || []);
      showResult("Product Service Response", data);
    } catch (error) {
      handleError("Product Service Error", error);
    } finally {
      setLoading(false);
    }
  };

  const registerUser = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username: "aigerim",
          password: "12345",
          email: "aigerim@example.com"
        })
      });
      const data = await response.json();
      showResult("Auth Service Registration Response", data);
    } catch (error) {
      handleError("Auth Service Error", error);
    } finally {
      setLoading(false);
    }
  };

  const loginUser = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username: "aigerim",
          password: "12345"
        })
      });
      const data = await response.json();
      showResult("Auth Service Login Response", data);
    } catch (error) {
      handleError("Auth Service Error", error);
    } finally {
      setLoading(false);
    }
  };

  const createOrder = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/orders`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username: "aigerim",
          product_id: 1,
          quantity: 2
        })
      });
      const data = await response.json();
      showResult("Order Service Response", data);
    } catch (error) {
      handleError("Order Service Error", error);
    } finally {
      setLoading(false);
    }
  };

  const processPayment = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/payments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          order_id: "demo-order-1",
          amount: 51.98,
          payment_method: "card"
        })
      });
      const data = await response.json();
      showResult("Payment Service Response", data);
    } catch (error) {
      handleError("Payment Service Error", error);
    } finally {
      setLoading(false);
    }
  };

  const sendNotification = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/notifications`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username: "aigerim",
          message: "Your cosmetics order has been processed successfully."
        })
      });
      const data = await response.json();
      showResult("Notification Service Response", data);
    } catch (error) {
      handleError("Notification Service Error", error);
    } finally {
      setLoading(false);
    }
  };

  const createReview = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/reviews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          product_id: 1,
          username: "aigerim",
          rating: 5,
          comment: "The hydrating cream is very nice."
        })
      });
      const data = await response.json();
      showResult("Review Service Response", data);
    } catch (error) {
      handleError("Review Service Error", error);
    } finally {
      setLoading(false);
    }
  };

  const checkHealth = async () => {
    try {
      setLoading(true);

      const endpoints = [
        "/auth-health",
        "/product-health",
        "/order-health",
        "/payment-health",
        "/notification-health",
        "/review-health"
      ];

      const results = {};

      for (const endpoint of endpoints) {
        const response = await fetch(endpoint);
        results[endpoint] = await response.json();
      }

      showResult("Microservices Health Check Response", results);
    } catch (error) {
      handleError("Health Check Error", error);
    } finally {
      setLoading(false);
    }
  };

  const buttons = [
    {
      label: "Register User",
      icon: <User size={18} />,
      action: registerUser
    },
    {
      label: "Login User",
      icon: <User size={18} />,
      action: loginUser
    },
    {
      label: "Load Products",
      icon: <Package size={18} />,
      action: loadProducts
    },
    {
      label: "Create Order",
      icon: <ShoppingBag size={18} />,
      action: createOrder
    },
    {
      label: "Process Payment",
      icon: <CreditCard size={18} />,
      action: processPayment
    },
    {
      label: "Send Notification",
      icon: <Bell size={18} />,
      action: sendNotification
    },
    {
      label: "Create Review",
      icon: <Star size={18} />,
      action: createReview
    },
    {
      label: "Check Health",
      icon: <Activity size={18} />,
      action: checkHealth
    }
  ];

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <div>
          <h1 style={styles.title}>Online Cosmetics Store</h1>
          <p style={styles.subtitle}>
            React + Nginx frontend for SRE microservices project
          </p>
        </div>
        <div style={styles.badge}>SRE Demo</div>
      </header>

      <main style={styles.main}>
        <section style={styles.hero}>
          <h2 style={styles.heroTitle}>Cosmetics Store Microservices Dashboard</h2>
          <p style={styles.heroText}>
            This frontend provides a single Nginx-based interface for testing
            Authentication, Product, Order, Payment, Notification, and Review services.
          </p>
        </section>

        <section style={styles.grid}>
          {buttons.map((button) => (
            <button
              key={button.label}
              onClick={button.action}
              style={styles.button}
              disabled={loading}
            >
              {button.icon}
              {button.label}
            </button>
          ))}
        </section>

        <section style={styles.contentGrid}>
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>Cosmetics Catalog</h3>

            {products.length === 0 ? (
              <p style={styles.emptyText}>
                Click “Load Products” to display cosmetics products.
              </p>
            ) : (
              <div style={styles.productGrid}>
                {products.map((product) => (
                  <div key={product.id} style={styles.productCard}>
                    <h4 style={styles.productName}>{product.name}</h4>
                    <p><strong>Brand:</strong> {product.brand}</p>
                    <p><strong>Category:</strong> {product.category}</p>
                    <p><strong>Price:</strong> ${product.price}</p>
                    <p><strong>Stock:</strong> {product.stock}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div style={styles.card}>
            <h3 style={styles.cardTitle}>API Response</h3>
            <pre style={styles.output}>{loading ? "Loading..." : output}</pre>
          </div>
        </section>
      </main>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #fff1f5 0%, #fdf2f8 50%, #ffffff 100%)",
    color: "#2d2d2d",
    fontFamily: "Arial, sans-serif"
  },
  header: {
    background: "#be185d",
    color: "white",
    padding: "28px 48px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    boxShadow: "0 4px 12px rgba(0,0,0,0.15)"
  },
  title: {
    margin: 0,
    fontSize: "32px"
  },
  subtitle: {
    margin: "8px 0 0",
    fontSize: "16px",
    opacity: 0.95
  },
  badge: {
    background: "white",
    color: "#be185d",
    padding: "10px 16px",
    borderRadius: "999px",
    fontWeight: "bold"
  },
  main: {
    maxWidth: "1200px",
    margin: "0 auto",
    padding: "32px"
  },
  hero: {
    background: "white",
    borderRadius: "20px",
    padding: "28px",
    marginBottom: "24px",
    boxShadow: "0 8px 24px rgba(0,0,0,0.08)"
  },
  heroTitle: {
    margin: "0 0 12px",
    color: "#be185d"
  },
  heroText: {
    margin: 0,
    lineHeight: 1.6
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "14px",
    marginBottom: "24px"
  },
  button: {
    border: "none",
    background: "#db2777",
    color: "white",
    padding: "14px 16px",
    borderRadius: "14px",
    cursor: "pointer",
    fontWeight: "bold",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
    boxShadow: "0 4px 12px rgba(219,39,119,0.25)"
  },
  contentGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(360px, 1fr))",
    gap: "24px"
  },
  card: {
    background: "white",
    borderRadius: "20px",
    padding: "24px",
    boxShadow: "0 8px 24px rgba(0,0,0,0.08)"
  },
  cardTitle: {
    marginTop: 0,
    color: "#be185d"
  },
  emptyText: {
    color: "#666"
  },
  productGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "14px"
  },
  productCard: {
    background: "#fff1f5",
    borderRadius: "14px",
    padding: "16px",
    border: "1px solid #fbcfe8"
  },
  productName: {
    marginTop: 0,
    color: "#be185d"
  },
  output: {
    background: "#111827",
    color: "#d1fae5",
    padding: "16px",
    borderRadius: "14px",
    minHeight: "280px",
    overflowX: "auto",
    whiteSpace: "pre-wrap"
  }
};

export default App;