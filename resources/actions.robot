*** Settings ***
Library  dut.dut.DUT  WITH NAME  DUT

*** Keywords ***
Select Product From Product Table
    [Arguments]  ${product_id}
    DUT.Select Product To Add   ${product_id}

Select Product From Selected Product Table
    [Arguments]  ${product_id}
    DUT.Select Product To Remove  ${product_id}

Press Select Button
    DUT.Press Add Product

Press Remove Button
    DUT.Press Remove Product

Press Checkout Button
    DUT.Press Checkout

Press Empty Cart Button
    DUT.Press Empty Cart

Press Finish Checkout Button
    DUT.Press Finish Checkout

Initialize DUT
    DUT.Initialize