"use client";
import { signIn, signOut, useSession } from "next-auth/react";
import Link from "next/link";
import React from "react";

const AppBar = () => {
    const { data: session } = useSession();

    return(
        <div>
            <div>
                {
                    session?.user ? (
                        <>
                            <p > {session.user.name}</p>
                            <button  onClick={() => signOut()}>Sign Out</button>
                        </>
                    ): (
                        <button onClick={() => signIn()}>Sign In</button>
                    )
                }
            </div>
        </div>
    );
}

export default AppBar;
