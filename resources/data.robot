*** Settings ***
Library   Collections
Library   dut.dut.DUT   WITH NAME   DUT

*** Keywords ***
Select Available Product ID
    ${available_products}   DUT.Get Available Products
    ${SELECTED_PRODUCT}     Evaluate  random.choice($available_products)   random
    Set Suite Variable  ${SELECTED_PRODUCT}

Select Product ID To Remove
    ${selected_products}    DUT.Get Selected Products
    ${PRODUCT_TO_REMOVE}     Evaluate  random.choice($selected_products)   random
    Set Suite Variable  ${PRODUCT_TO_REMOVE}
