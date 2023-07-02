"use client";

import React from 'react'
import { useRouter } from 'next/navigation'
import Image from 'next/image';

import { signIn, signOut, useSession } from 'next-auth/react'

export default function Home() {
    const { data: session } = useSession()
    console.log(session)
    const router = useRouter()

  return (
    <div className='bg-emerald-600'> 
        <div className='flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0'>
            <Image src="/images/logo_white.png" alt="logo" width={150} height={80} className='pb-4' />
            <a href="#" className='flex items-center mb-6 text-2xl font-semibold text-white'>
                Rescate de Flora y Fauna
            </a>
            <div className='w-full bg-white rounded-lg shadow md:mt-0 sm:max-w-md xl:p-0'>
                <div className='p-6 space-y-4 md:space-y-6 sm:p-8'>
                    <h1 className='text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl'>
                        Iniciar Sesión
                    </h1>
                    <form className='space-y-4 md:space-y-6'>
                        <div >
                            <label className='block mb-2 text-sm font-medium text-gray-900' >Correo electronico</label>
                            <input 
                                type='email'
                                className='bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'
                            />
                        </div>
                        <div>
                            <label className='block mb-2 text-sm font-medium text-gray-900' >Contraseña</label>
                            <input 
                                type='password'
                                className='bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5'
                             />
                        </div>
                        <div className='flex items-center justify-between' >
                            <a className='text-sm font-medium text-primary-600 hover:underline'>Olvide mi contraseña</a>
                        </div>
                                <button type="button" onClick={()=> router.push('/dashboard')}>
                                    LOGIN
                                </button>
                                <a href="/">¿Olvidaste tu contraseña?</a>
                        </form>

                    </div>

                </div>
            </div>
        </div>
  )
}
