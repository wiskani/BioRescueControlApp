'use client'

import { useRouter } from 'next/navigation';

import { useState, useEffect } from 'react';

const SpecieItem = (props: SpecieItemData) => {
    const imageUrl = props.images && props.images.length > 0 ? `${process.env.NEXT_PUBLIC_API_URL}:8080${props.images[0].url}` : `${process.env.NEXT_PUBLIC_API_URL}:8080/static/images/species/no_imagen.svg`;
    const imageTitle = props.images && props.images.length > 0 ? props.images[0].atribute : 'No hay imagen';
    
    const [statusColor, setStatusColor] = useState('bg-green-600');

    useEffect(() => {
        switch (props.status_name) {
            case 'Preocupación menor':
                setStatusColor('text-green-600');
                break;
            case 'Casi amenazada':
                setStatusColor('text-yellow-600');
                break;
            case 'Vulnerable':
                setStatusColor('text-orange-500');
                break;
            case 'En peligro':
                setStatusColor('text-red-600');
                break;
            default:
                setStatusColor('text-gray-500');
                break;
        }

    }
    , [props.status_name]);
        


    const router = useRouter();

    return (
        <section
            className="text-gray-700 body-font overflow-hidden bg-white"
        >
            <div
                className="container px-5 py-5 mx-auto"
            >
                <div
                    className="mx-auto flex flex-wrap"
                >
                    <img
                        alt="specie"
                        title={imageTitle}
                        className="
                        lg:w-1/2
                        w-full
                        object-cover
                        object-center
                        rounded
                        border
                        border-gray-200
                        "
                        src={imageUrl}
                    />
                    <div className="w-full mt-6 ">
                        <h1
                            className="
                            text-gray-900
                            text-xl
                            title-font
                            font-medium mb-1"
                        >
                            Especie: {props.specie_name}
                        </h1>
                        <h2
                            className="
                            text-sm
                            title-font
                            text-gray-500
                            tracking-widest
                            "
                        >
                            Genero: {props.genus_full_name}
                        </h2>
                        <h3
                            className="
                            text-xs
                            title-font
                            text-gray-500
                            tracking-widest"
                        >
                            Familia: {props.family_name}
                        </h3>
                        <h3
                            className="
                            text-xs
                            title-font
                            text-gray-500
                            tracking-widest
                            "
                        >
                            Orden: {props.order_name}
                        </h3>
                        <h3
                            className="
                            text-xs
                            title-font
                            text-gray-500
                            tracking-widest
                            "
                        >
                            Clase: {props.class_name}
                        </h3>
                        {
                            props.status_name?
                            <h3
                                className='
                                text-xs
                                title-font
                                text-gray-500
                                tracking-widest
                                '
                            >
                                Estado de Conservación: 
                                    <p
                                        className={`
                                            ${statusColor}
                                            italic
                                        `}
                                    >
                                        {props.status_name}
                                    </p>
                                </h3>
                            : null

                        }
                        <div
                            className="
                            flex
                            mt-6
                            items-center
                            pb-5
                            border-b-2
                            border-gray-200
                            mb-5
                            "
                        >
                            <div className="flex">
                                <span
                                    className="mr-3"
                                >
                                    Cantidad de Rescates
                                </span>
                                <button
                                    className="
                                    flex
                                    items-center
                                    bg-green-600
                                    text-center
                                    text-xs
                                    text-white
                                    justify-center
                                    border-2
                                    border-gray-300
                                    rounded-full
                                    w-6
                                    h-6
                                    focus:outline-none
                                    "
                                    type="button"
                                    onClick={
                                        () => router.push(
                                            `/dashboard/rescues/${props.id}`
                                        )
                                    }
                                >
                                    {props.total_rescues}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default SpecieItem;
