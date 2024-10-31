import React from 'react';
import { Button } from 'devextreme-react/button';
import { TextBox } from 'devextreme-react/text-box';
import { Validator, RequiredRule } from 'devextreme-react/validator';

function LogIn() {
    return (
        <form action="/Login" method="post">
            Username:
            <TextBox name="Login">
                <Validator>
                    <RequiredRule />
                </Validator>
            </TextBox>
            Password:
            <TextBox name="Password" mode="password">
                <Validator>
                    <RequiredRule />
                </Validator>
            </TextBox>
            <Button
                text="Submit"
                type="success"
                useSubmitBehavior={true}
            />
        </form>
    );
}

export default LogIn;
