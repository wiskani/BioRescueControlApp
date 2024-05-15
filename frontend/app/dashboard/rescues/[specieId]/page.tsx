"use client"

//Next imports
import dynamic from 'next/dynamic'
import { useSession  } from 'next-auth/react'
import { useRouter } from 'next/navigation';


//React imports
import React,{useEffect, useState, useCallback}  from 'react';

//Table imports
import { createColumnHelper } from '@tanstack/react-table';

//Api imports
import { GetRescuesSpecie } from "@/app/libs/species/ApiSpecies"

//Componest imports
import { TableSimple } from '@/app/components/Table/TableSimple';
import { LineProyect } from '@/app/components/Map/lineProyect';
import Legend from '@/app/components/Map/Legend';
import FloraRescueSpecieMap from '@/app/components/RescueFlora/rescueFloraSpecieMap'; 
import TransectHerpetofaunaSpecieMap from '@/app/components/HerpetoFauna/TransectoSpecieMap';
import RescueMammalsSpecieMap from '@/app/components/RescueMammals/RescueMammalsSpecieMap';

//service imports
import { dateFormat } from '@/app/services/dateFormat';

//Leaflet dynamic imports
const MapContainer = dynamic(
    async () => (await import('react-leaflet')).MapContainer,
    { ssr: false }  
)

const TileLayer = dynamic(
    async () => (await import('react-leaflet')).TileLayer,
    { ssr: false }
)

const Polyline = dynamic(
    async () => (await import('react-leaflet')).Polyline,
    { ssr: false }
)

const Tooltip = dynamic(
    async () => (await import('react-leaflet')).Tooltip,
    { ssr: false }
)

const Pane = dynamic(
    async () => (await import('react-leaflet')).Pane,
    { ssr: false }
)


//types
type RescuesSpecieData =
| FloraRescueSpeciesData
| TransectHerpetoWithSpeciesData
| RescueMammalsWithSpecieData 

//predicados fuctions
function isFloraRescueSpeciesData(
    data: RescuesSpecieData
): data is FloraRescueSpeciesData {
    return  data && "epiphyte_number" in data;
}

function isTransectHerpetoWithSpeciesData(
    data: RescuesSpecieData
): data is TransectHerpetoWithSpeciesData {
    return  data && "number" in data;
}

function isRescueMammalsWithSpecieData(
    data: RescuesSpecieData
): data is RescueMammalsWithSpecieData {
    return  data && "cod" in data;
}

export default function Page({ params} : { params: { specieId: number } }) {
    const { data: session } = useSession();
    const user = session?.user;
    const [rescues, setRescues] = useState<RescuesSpecieData[]>([]);
    const [errorMessage, SetErrorMessage]= useState<string>();
    const router = useRouter();

    //For map
    const lineOptions = { color: 'red' }
    const legendOptions : () => string[] = () => {
        if (isFloraRescueSpeciesData(rescues[0])) {
            return ['blue', 'red' ]
        }
        if (isTransectHerpetoWithSpeciesData(rescues[0])) {
            return ['green', 'red' ]
        }
        if (isRescueMammalsWithSpecieData(rescues[0])) {
            return ['brown', 'red' ]
        }
        return ['red' ]
    }

    const legendLabels: () => string[] = () => {
        if (isFloraRescueSpeciesData(rescues[0])) {
            return [
                'puntos rescates de flora',
                'proyecto 230 kv mizque - sehuencas'
            ]
        }
        if (isTransectHerpetoWithSpeciesData(rescues[0])) {
            return [
                'transcetors herpetofauna',
                'proyecto 230 kv mizque - sehuencas'
            ]
        }
        if (isRescueMammalsWithSpecieData(rescues[0])) {
            return [
                'puntos rescate de mamiferos',
                'proyecto 230 kv mizque - sehuencas'
            ]
        }
        return ['proyecto 230 kv mizque - sehuencas']
    }


    //Obtain data from api
    const rescuesData = useCallback(
        async (): Promise<RescuesSpecieData[]> => {
            if (user) {
                try {
                    const data = await GetRescuesSpecie({
                        token: user?.token,
                        specie_id: params.specieId
                    });
                    return data;
                } catch (error) {
                    if (error instanceof Error) {
                        SetErrorMessage(error.message);
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
            cell: info => dateFormat(info.getValue() as Date),
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
            cell: info => dateFormat(info.getValue() as Date),
            footer: info => info.column.id,
        }),
        columnHelper.accessor('date_out', {
            header: 'fecha de salida',
            cell: info => dateFormat(info.getValue() as Date),
            footer: info => info.column.id,
        }),
        columnHelper.accessor('specie_names', {
            header: 'especies',
            cell: info =>{
                const species  = info.getValue() as string[];
                return( 
                    <>
                        {
                            species.length > 0 ?
                                species[0] :
                                null
                        }
                    </>
                )
            },
            footer: info => info.column.id,
        }
        ),
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
            cell: info => dateFormat(info.getValue() as Date),
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
        <div>
            {
                isFloraRescueSpeciesData(rescues[0])
                    ? <h1
                        className="
                        m-4
                        text-gl
                        text-center
                        font-bold
                        leading-none
                        tracking-tight
                        text-gray-600
                        md:text-xl
                        lg:text-xl
                        dark:text-white
                        "
                    >Rescates para la especie
                        <span className='italic'> {rescues[0].specie_name}</span>
                    </h1>
                    : null
            }
            {
                isTransectHerpetoWithSpeciesData(rescues[0])
                    ? <h1
                        className="
                        m-4
                        text-gl
                        text-center
                        font-bold
                        leading-none
                        tracking-tight
                        text-gray-600
                        md:text-xl
                        lg:text-xl
                        dark:text-white
                        "
                    >Rescates para la especie 
                        <span className='italic'> {rescues[0].specie_names[0]}</span>
                    </h1>
                    : null
            }
            {
                isRescueMammalsWithSpecieData(rescues[0])
                    ? <h1
                        className="
                        m-4
                        text-gl
                        text-center
                        font-bold
                        leading-none
                        tracking-tight
                        text-gray-600
                        md:text-xl
                        lg:text-xl
                        dark:text-white
                        "
                    >Rescates para la especie
                        <span className='italic'> {rescues[0].specie_name}</span>
                    </h1>
                    : null
            }
            <div
                className="
                flex
                flex-col
                h-full
                2xl:mb-52
                xl:mb-52
                lg:mb-40
                md:flex-row
                md:mb-0
                sm:mb-0
                justify-center
                "
            >
                <div
                    className="
                    h-96
                    p-0
                    z-50
                    2xl:mb-52
                    xl:mb-52
                    lg:mb-40
                    md:w-1/2
                    p-4
                    md:h-[16rem]
                    sd:h-[6rem]
                    "
                >
                    <MapContainer
                        center={[-17.489, -65.271]}
                        zoom={12}
                        scrollWheelZoom={false}
                        className='
                        h-80
                        w-full
                        2xl:h-[40rem]
                        xl:h-[40rem]
                        lg:h-[35rem]
                        '
                    >
                        <TileLayer

                            url={`https://api.mapbox.com/styles/v1/mapbox/streets-v12/tiles/256/{z}/{x}/{y}@2x?access_token=${process.env.NEXT_PUBLIC_MAPBOX_TOKEN}`}
                            attribution='Map data &copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors, <a href=&quot;https://creativecommons.org/licenses/by-sa/2.0/&quot;>CC-BY-SA</a>, Imagery &copy; <a href=&quot;https://www.mapbox.com/&quot;>Mapbox</a>'
                        />
                        <Pane name='rescues' style={{zIndex:499}}>
                            {
                                isRescueMammalsWithSpecieData(rescues[0])
                                    ? <RescueMammalsSpecieMap data={rescues.filter(isRescueMammalsWithSpecieData)}/>
                                    : null
                            }
                            {
                                isTransectHerpetoWithSpeciesData(rescues[0])
                                    ?<TransectHerpetofaunaSpecieMap data={rescues.filter(isTransectHerpetoWithSpeciesData)}/>
                                    : null
                            }
                            {
                                isFloraRescueSpeciesData(rescues[0])
                                    ?<FloraRescueSpecieMap data={rescues.filter(isFloraRescueSpeciesData)}/>
                                    : null
                            }
                        </Pane>
                        <Pane name='linea' style={{zIndex:400}}>
                            <Polyline pathOptions={lineOptions} positions={LineProyect} >
                                <Tooltip>
                                    <div>
                                        <h4>Detalles</h4>
                                        <p>Proyecto 230 kV Mizque - Sehuencas</p>
                                    </div>
                                </Tooltip>
                            </Polyline>

                        </Pane>
                        <Legend colors={legendOptions()} labels={legendLabels()} />
                    </MapContainer>
                </div>
            </div>
            <div className="container mx-auto px-4 py-20">
                {renderTable()}
            </div>
            <button 
                type="button"
                onClick={() => router.back()}
                className="bg-emerald-900  hover:bg-emerald-500 text-white font-bold py-2 px-4 rounded"
            >
                Volver
            </button>
        </div>

    )
}

