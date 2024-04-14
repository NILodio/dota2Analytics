import {
  Container,
  Flex,
  Heading,
  Spinner,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"

import { PollsService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"
import useCustomToast from "../../hooks/useCustomToast"

export const Route = createFileRoute("/_layout/polls")({
  component: Polls,
})

function Polls() {
  const showToast = useCustomToast()
  const {
    data: polls,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["polls"],
    queryFn: () => PollsService.readPolls({}),
  })

  if (isError) {
    const errDetail = (error as any).body?.detail
    showToast("Something went wrong.", `${errDetail}`, "error")
  }

  return (
    <>
      {isLoading ? (
        // TODO: Add skeleton
        <Flex justify="center" align="center" height="100vh" width="full">
          <Spinner size="xl" color="ui.main" />
        </Flex>
      ) : (
        polls && (
          <Container maxW="full">
            <Heading
              size="lg"
              textAlign={{ base: "center", md: "left" }}
              pt={12}
            >
              Poll Heroes
            </Heading>
            <Navbar type={"Poll"} />
            <TableContainer>
              <Table size={{ base: "sm", md: "md" }}>
                <Thead>
                  <Tr>
                    <Th>ID</Th>
                    <Th>Hero ID</Th>
                    <Th>Hero Name</Th>
                    <Th>Team</Th>
                    <Th>Team ID</Th>
                    <Th>Player</Th>
                    <Th>Description</Th>
                    <Th>Actions</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {polls.data.map((poll) => (
                    <Tr key={poll.id}>
                      <Td>{poll.id}</Td>
                      <Td>{poll.hero_id}</Td>
                      <Td>{poll.hero_name}</Td>
                      <Td>{poll.team}</Td>
                      <Td>{poll.team_id}</Td>
                      <Td>{poll.player_name}</Td>
                      <Td color={!poll.description ? "ui.dim" : "inherit"}>
                        {poll.description || "N/A"}
                      </Td>
                      <Td>
                        <ActionsMenu type={"Poll"} value={poll} />
                      </Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </TableContainer>
          </Container>
        )
      )}
    </>
  )
}
