*** Settings ***
Resource   resources/verifiers.robot

*** Keywords ***
Verify Init Predicates
    Log  Init State Passed

Verify Empty Cart Predicates
    Verify Cart Is Empty
    Verify Empty Cart Button Is Not Visible
    Verify Checkout Button Is Not Visible
    Verify Remove Product Button Is Not Visible
    Verify Add Product Button Is Visible

Verify Product Added Predicates
    Verify Product Number Increased
    Verify Empty Cart Button Is Visible
    Verify Checkout Button Is Visible
    Verify Remove Product Button Is Visible
    Verify Add Product Button Is Visible

Verify Product Removed Predicates
    Verify Product Number Decreased
    Verify Empty Cart Button Is Visible
    Verify Checkout Button Is Visible
    Verify Add Product Button Is Visible
    Verify Remove Product Button Is Visible

Verify Checkout Predicates
    Verify Empty Cart Button Is Visible
    Verify Checkout Button Is Not Visible
    Verify Remove Product Button Is Not Visible
    Verify Add Product Button Is Not Visible