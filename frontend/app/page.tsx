"use client";

import { useSession  } from 'next-auth/react'
import React from 'react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import Map from './components/Map/Map';

const MyMap =  dynamic(() => import('./components/Map/Map'), {ssr: false});

export default function HomePage() {
    const router = useRouter();
    const { data: session } = useSession();
    if (session?.user) {
        return (
            <div>
                <h1>Home Page</h1>
                <MyMap/>
                <p>{process.env.MAPBOX_TOKEN}</p>
                <p>prueba</p>
            </div>
        )
    }
    return (
        <div>
            <h1> Debes iniciar session</h1>
        </div>
    )
}
