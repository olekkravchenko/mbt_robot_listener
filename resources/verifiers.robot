*** Settings ***
Library  dut.dut.DUT  WITH NAME  DUT

*** Variables ***
${CURRENT_PRODUCT_NUMBER}   0


*** Keywords ***
Verify Cart Is Empty
    ${product_number}  DUT.Get Selected Product Number
    Should Be Equal As Integers  ${product_number}  0
    Set Suite Variable  ${CURRENT_PRODUCT_NUMBER}   0

Verify Cart Item Number
    [Arguments]   ${expected_number}
    Log  ${expected_number}

Verify Empty Cart Button Is Not Visible
    ${is_visible}  DUT.Empty Cart Button Is Visible
    Should Not Be True    ${is_visible}

Verify Empty Cart Button Is Visible
    ${is_visible}  DUT.Empty Cart Button Is Visible
    Should Be True  ${is_visible}

Verify Checkout Button Is Not Visible
    ${is_visible}  DUT.Checkout Button Is Visible
    Should Not Be True  ${is_visible}

Verify Checkout Button Is Visible
    ${is_visible}  DUT.Checkout Button Is Visible
    Should Be True  ${is_visible}

Verify Remove Product Button Is Visible
    ${is_visible}  DUT.Remove Product Button Is Visible
    Should Be True  ${is_visible}
    
Verify Remove Product Button Is Not Visible
    ${is_visible}  DUT.Remove Product Button Is Visible
    Should Not Be True  ${is_visible}
    
Verify Add Product Button Is Visible
    ${is_visible}  DUT.Add Product Button Is Visible
    Should Be True  ${is_visible}
    
Verify Add Product Button Is Not Visible
    ${is_visible}  DUT.Add Product Button Is Visible
    Should Not Be True  ${is_visible}
        
Verify Product Number Increased
    ${product_number}  DUT.Get Selected Product Number
    Should Be Equal As Integers  ${product_number}  ${${CURRENT_PRODUCT_NUMBER}+1}
    Set Suite Variable  ${CURRENT_PRODUCT_NUMBER}  ${product_number}

Verify Product Number Decreased
    ${product_number}  DUT.Get Selected Product Number
    Should Be Equal As Integers  ${product_number}  ${${CURRENT_PRODUCT_NUMBER}-1}
    Set Suite Variable  ${CURRENT_PRODUCT_NUMBER}  ${product_number}