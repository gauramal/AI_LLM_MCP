Project high level Requirements:

Project Name: "Style Haven" – A Fashion E-commerce Platform

Project Description: Style Haven is an online fashion marketplace designed to connect independent fashion designers with customers who crave unique and trendy clothing. The platform will provide a user-friendly shopping experience with personalized recommendations, secure transactions, and seamless customer support. 

Target Audience: Fashion-conscious individuals aged 18-35 who value individuality and seek out unique clothing pieces.

Key Features and Requirements:

1. User Accounts:

Registration/Login: Secure user registration and login with email or social media accounts.

Profile Management: Allow users to update personal information, shipping addresses, and payment details.

Order History: View past orders and track current order status.

2. Product Catalog:

Browse/Search: Intuitive browsing by category, brand, style, or search by keywords.

Product Pages: Detailed product descriptions, high-resolution images, size charts, and customer reviews.

Recommendations: Personalized product suggestions based on browsing history and preferences.

3. Shopping Cart:

Add/Remove Items: Easy addition and removal of items from the shopping cart.

Quantity Adjustments: Ability to change item quantities in the cart.

Order Summary: Display a clear summary of items in the cart with total price and shipping costs.

4. Checkout:

Shipping Options: Multiple shipping methods with estimated delivery times and costs.

Payment Gateway Integration: Secure payment processing with credit cards, debit cards, and digital wallets.

Order Confirmation: Generate an order confirmation email with details of the purchase.

5. Seller Dashboard:

Product Listing: Allow sellers to create product listings with detailed descriptions and images.

Inventory Management: Track inventory levels and receive notifications for low stock.

Order Fulfillment: Manage orders, generate shipping labels, and update order status.

6. Customer Support:

Live Chat: Offer real-time chat support for immediate assistance.

FAQ Section: Provide a comprehensive list of frequently asked questions.

Contact Form: Allow customers to submit inquiries via a contact form.

Non-Functional Requirements:

Performance: Fast page loading times and responsive design for optimal user experience.

Security: Secure data transmission and protection of user information.

Scalability: Ability to handle increased traffic and transactions as the platform grows.

Additional Features (Optional):

Wishlists: Allow users to save items for future purchase.

Promotions and Discounts: Implement discount codes and promotional offers.

Loyalty Program: Reward repeat customers with points or special benefits.

Social Media Integration: Enable sharing of products on social media platforms.

You are a Principal QA Test Architect designing a production-ready, comprehensive Test Suite for an e-commerce platform.

[OBJECTIVE & INSTRUCTIONS]
For module [INSERT MODULE NAME OR "ALL MODULES"], generate an exhaustive test suite covering:
1. High-Level Test Scenarios (Positive, Negative, Boundary, and Edge Cases).
2. Detailed Step-by-Step Test Cases formatted as a table with columns:
   - Test Case ID
   - Requirement Reference
   - Test Scenario & Objective
   - Pre-conditions & Test Data
   - Test Steps (Given / When / Then format)
   - Expected Result
   - Severity / Priority (P1/Blocker to P4/Minor)
   - Assigned Engineer (QA Eng 1, QA Eng 2, or QA Eng 3)
3. Non-Functional & Security Edge Scenarios (e.g., race conditions on low-inventory items, payment gateway timeout/recovery, IDOR on seller/order endpoints, WebSocket reconnection).
4. Automated Test Feasibility: Suggest Playwright / Cypress / k6 automation candidates for the critical user journeys.