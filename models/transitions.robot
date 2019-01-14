*** Settings ***
Resource    resources/actions.robot
Resource    resources/data.robot

*** Keywords ***
Transition From Initial To Empty Cart
    Log   Move to Empty Cart

Transition To Product Added
    Select Available Product ID
    Select Product From Product Table  ${SELECTED_PRODUCT}
    Press Select Button

Transition To Product Removed
    Select Product ID To Remove
    Select Product From Selected Product Table  ${PRODUCT_TO_REMOVE}
    Press Remove Button

Transition To Empty Cart
    Press Empty Cart Button

Transition To Checkout
    Press Checkout Button

Transition From Checkout To Empty Cart
    Press Finish Checkout Button

Cleanup
    Initialize DUT