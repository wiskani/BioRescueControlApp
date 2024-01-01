"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { useRouter } from 'next/navigation';


//React imports
import React,{useEffect, useState, useCallback}  from 'react';

//Table imports
import { createColumnHelper } from '@tanstack/react-table';

//Api imports
import { ApiRescuesSpecie } from "@/app/api/species/route"

//Componest imports
import { TableSimple } from '@/app/components/Table/TableSimple';

//types
type RescuesSpecieData =
        | FloraRescueSpeciesData
        | TransectHerpetoWithSpeciesData
        | RescueMammalsWithSpecieData 

//predicados fuctions
function isFloraRescueSpeciesData(data: RescuesSpecieData): data is FloraRescueSpeciesData {
    return  data && "epiphyte_number" in data;
}

function isTransectHerpetoWithSpeciesData(data: RescuesSpecieData): data is TransectHerpetoWithSpeciesData {
    return  data && "number" in data;
}

function isRescueMammalsWithSpecieData(data: RescuesSpecieData): data is RescueMammalsWithSpecieData {
    return  data && "cod" in data;
}
        
export default function Page({ params} : { params: { specieId: number } }) {
    const { data: session } = useSession();
    const user = session?.user;
    const [rescues, setRescues] = useState<RescuesSpecieData[]>([]);
    const [errorMessage, SetErrorMessage]= useState<string>();
    const router = useRouter();

    //Obtain data from api
    const rescuesData = useCallback(async (): Promise<RescuesSpecieData[]> => {
            if (user) {
                    try {
                        const data = await ApiRescuesSpecie({ token: user?.token, specie_id: params.specieId });
                        return data;
                    } catch (error) {
                            if (error instanceof Error) {
                                SetErrorMessage(error.message);
                                console.error('Error:', error.message);
                                return [];
                            }
                        return [];
                    }
            }
            else {
                return [];
                }
                }, [user, params.specieId]);

    useEffect(() => {
                        rescuesData().then((data) => {
                                setRescues(data);
                                });
                        }, [session, rescuesData]);



    const renderTable = () => {
            if (rescues.length > 0) {
                    if (isFloraRescueSpeciesData(rescues[0])) {
                            return(
                                <TableSimple<RescuesSpecieData>
                                        columns={columnsFlora}
                                        data={rescues}
                                /> 
                                )
                        }
                        else if (isTransectHerpetoWithSpeciesData(rescues[0])) {
                                return(
                                <TableSimple<RescuesSpecieData>
                                        columns={columnsHerpeto}
                                        data={rescues}
                                /> 
                                )
                        }
                        else if (isRescueMammalsWithSpecieData(rescues[0])) {
                                return(
                                <TableSimple<RescuesSpecieData>
                                        columns={columnsMammals}
                                        data={rescues}
                                /> 
                                )
                        }

        }
        else {
                return (
                <div>

                        <p>{errorMessage}</p>
                </div>
                )
        }

    }
    //make columns
    const columnHelper = createColumnHelper<RescuesSpecieData>();

    const columnsFlora = [
        columnHelper.accessor('epiphyte_number', {
                        header: 'Número de epífito',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('rescue_date', {
                        header: 'Fecha de rescate',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('specie_name', {
                        header: 'Especie',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('genus_name', {
                        header: 'Género',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('family_name', {
                        header: 'Familia',
                        footer: info => info.column.id,
                }),
    ]
    const columnsHerpeto = [
        columnHelper.accessor('number', {
                        header: 'Número de Transecto ',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('date_in', {
                        header: 'Fecha de entrada',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('date_out', {
                        header: 'fecha de salida',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('specie_names', {
                        header: 'especies',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('total_rescue', {
                        header: 'Cantidad de rescates',
                        footer: info => info.column.id,
                }),
    ]
    const columnsMammals = [
        columnHelper.accessor('cod', {
                header: 'Código',
                footer: info => info.column.id,
        }),
        columnHelper.accessor('date', {
                header: 'Fecha',
                footer: info => info.column.id,
        }),
        columnHelper.accessor('specie_name', {
                header: 'Especie',
                footer: info => info.column.id,
        }),
        columnHelper.accessor('observation', {
                header: 'Observación',
                footer: info => info.column.id,
        }),
        ]



        return (
        <>
        <div>
            <div>
            {user 
            ? renderTable()
             
            : <p>inicia sesión</p>
            }
            </div>
            <button 
                type="button"
                onClick={() => router.back()}
                className="bg-emerald-900  hover:bg-emerald-500 text-white font-bold py-2 px-4 rounded"
            >
                Volver
            </button>
        </div>
            
        </>
        )
        }

