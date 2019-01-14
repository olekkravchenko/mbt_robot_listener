*** Settings ***
Library  dut.dut.DUT  WITH NAME   DUT

*** Keywords ***
Only One Item Available
    [Tags]  precondition
    ${selected_product_number}  DUT.Get Selected Product Number
    Should Be Equal As Integers  ${selected_product_number}   1    msg=Precondition Failure

More Than One Item Available
    [Tags]  precondition
    ${selected_product_number}  DUT.Get Selected Product Number
    Should Not Be Equal As Integers  ${selected_product_number}   1   msg=Precondition Failure