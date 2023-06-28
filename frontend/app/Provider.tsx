"use client";
import { SessionProvider } from "next-auth/react";
import React, { ReactNode } from "react";

interface Props {
    children: ReactNode;
}
function Provider({ children }: Props) {
    return (
        <SessionProvider session={null}>
            {children}
        </SessionProvider>
    );
}   
export default Provider;