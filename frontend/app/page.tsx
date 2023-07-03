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
                <p>Signed in as {session.user.name}</p>
            </div>
        )
    }
    return (
        <div>
            <button onClick={() => router.push('/login')}>Sign in</button>
        </div>
    )
}
