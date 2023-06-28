"use client";
import { signIn, signOut, useSession } from "next-auth/react";
import Link from "next/link";
import React from "react";

const AppBar = () => {
    const { data: session } = useSession();

    return(
    )