"use client"

import { 
    Admin, 
    Resource, 
    ListGuesser, 
    EditGuesser,
    SimpleList,
} from 'react-admin'
import { useMediaQuery, Theme } from '@mui/material'
import JsonServerProvider from 'ra-data-json-server'

import { UserList } from './Users'

const resourceUrl = process.env.RESOURCE_URL 
    || 'https://jsonplaceholder.typicode.com'

const dataProvider = JsonServerProvider(resourceUrl)

const AdminApp = () => {
	//const isSmall = useMediaQuery<Theme>((theme)=> theme.breakpoints.down('sm'))

	return /*isSmall ? (
		<SimpleList
		  primaryText={(record)=> record.name}
		  secondaryText={(record) =>record.userName}
		  tertiaryText={(record)=>record.email}
		/>
	) :*/ (
    <Admin dataProvider={dataProvider}>
      <Resource 
          name="users"
	  list={UserList}
	  edit={EditGuesser}
	  recordRepersentation="name"
      />
      <Resource
          name="posts"
	  list={ListGuesser}
	  edit={EditGuesser}
	  recordRepersentation="name"
      />
      <Resource 
          name="comments" 
	  list={ListGuesser} 
	  edit={EditGuesser} 
      />
      <Resource
          name="albums" 
	  list={ListGuesser} 
	  edit={EditGuesser} 
      /> 
      <Resource
          name="photos" 
	  list={ListGuesser} 
	  edit={EditGuesser} 
      />
      <Resource
          name="todos" 
	  list={ListGuesser} 
	  edit={EditGuesser} 
      />
    </Admin>
  )
}

export default AdminApp
