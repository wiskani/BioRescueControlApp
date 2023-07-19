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
            <div className="relative w-full h-96">
                <div className='absolute top-0 left-0 w-full h-full'>
                    <MyMap/>
                </div>
            </div>
        )
    }
    return (
        <div>
            <h1> Debes iniciar session</h1>
        </div>
    )
}
