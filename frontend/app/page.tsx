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
            <div className="flex flex-col md:flex-row justify-center">
                <div className="h-[24rem] z-50 md:w-1/2 p-4">
                    <MyMap/>
                </div>
                <div className='md:w-1/2 p-4'>
                    <h1> Hola datos </h1>
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
