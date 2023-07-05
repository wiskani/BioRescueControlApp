"use client";

import { useSession  } from 'next-auth/react'
import React from 'react';
import { useRouter } from 'next/navigation';
export default function HomePage() {
    const router = useRouter();
    const { data: session } = useSession();
    if (session?.user) {
        return (
            <div>
                <h1>Home Page</h1>
            </div>
        )
    }
    return (
        <div>
            <h1> Debes iniciar session</h1>
        </div>
    )
}
