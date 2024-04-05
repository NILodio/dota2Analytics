import { Button, Flex, Icon, useDisclosure } from "@chakra-ui/react"
import { FaPlus } from "react-icons/fa"

import AddUser from "../Admin/AddUser"
import AddItem from "../Items/AddItem"

interface NavbarProps {
  type: string
}

const Navbar = ({ type }: NavbarProps) => {
  const addUserModal = useDisclosure()
  const addItemModal = useDisclosure()

  return (
    <>
      <Flex py={8} gap={4}>
        <Button
          variant="primary"
          gap={1}
          fontSize={{ base: "sm", md: "inherit" }}
          onClick={type === "User" ? addUserModal.onOpen : addItemModal.onOpen}
        >
          <Icon as={FaPlus} /> Add {type}
        </Button>
        <AddUser isOpen={addUserModal.isOpen} onClose={addUserModal.onClose} />
        <AddItem isOpen={addItemModal.isOpen} onClose={addItemModal.onClose} />
      </Flex>
    </>
  )
}

export default Navbar
