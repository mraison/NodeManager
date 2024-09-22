from NodeManager.chunker.model import Address, Device, AddressChunker, AddressChunk, DeviceChunkGroup


def get_dummy_input():
    return [
        Device(
            id=1,
            name="panic button",
            subscribers=[
                Address(
                    id=1,
                    name="John Doe",
                    email="dummy@fake.com"
                ),
            ]
        ),
        Device(
            id=2,
            name="warn button",
            subscribers=[
                Address(
                    id=1,
                    name="John Doe",
                    email="dummy@fake.com"
                ),
                Address(
                    id=2,
                    name="janedoe",
                    email="janedoe@dummy.com"
                )
            ]
        )
    ]


class TestAddressChunker:
    def test_get_chunks(self):
        chunker = AddressChunker(5)
        chunks = chunker.get_chunks()

        assert len(chunks) == 5
        for chunk in chunks:
            assert chunk.subscribers == set()

    def test_distribute_addresses(self):
        expected = [
            AddressChunk(
                subscribers=set([
                    Address(
                        id=1,
                        name="John Doe",
                        email="dummy@fake.com"
                    )
                ])
            ),
            AddressChunk(
                subscribers=set([
                    Address(
                        id=2,
                        name="janedoe",
                        email="janedoe@dummy.com"
                    )
                ])
            )
        ]

        chunker = AddressChunker(2)
        chunker.distribute_addresses(
            [
                Address(
                    id=1,
                    name="John Doe",
                    email="dummy@fake.com"
                ),
                Address(
                    id=2,
                    name="janedoe",
                    email="janedoe@dummy.com"
                )
            ]
        )
        actual = chunker.get_chunks()

        assert expected.sort() == actual.sort()

    def test_clear_chunks(self):
        chunker = AddressChunker(2)
        chunker.distribute_addresses(
            [
                Address(
                    id=1,
                    name="John Doe",
                    email="dummy@fake.com"
                ),
                Address(
                    id=2,
                    name="janedoe",
                    email="janedoe@dummy.com"
                )
            ]
        )
        chunks = chunker.get_chunks()
        assert len(chunks) == 2
        for chunk in chunks:
            assert len(chunk.subscribers) > 0

        chunker.clear_chunks()
        chunks = chunker.get_chunks()
        for chunk in chunks:
            assert len(chunk.subscribers) == 0


class TestDeviceChunkGroup:
    def test_create_device(self):
        d = Device(
            id=1,
            name="dummy",
            subscribers=[
                Address(
                    id=1,
                    name="John Doe",
                    email="dummy@fake.com"
                )
            ]
        )

        dcg = DeviceChunkGroup(1)
        dcg.create_device(d)
        chunks = dcg.get_chunk_group(1)

        assert len(chunks.get_chunks()) == 1

    def test_delete_device(self):
        d = Device(
            id=1,
            name="dummy",
            subscribers=[
                Address(
                    id=1,
                    name="John Doe",
                    email="dummy@fake.com"
                )
            ]
        )

        dcg = DeviceChunkGroup(1)
        dcg.create_device(d)
        chunks = dcg.get_chunk_group(1)

        assert len(chunks.get_chunks()) == 1

        dcg.delete_device(d)
        assert dcg.get_chunk_group(1) is None

    def test_update_device(self):
        d = Device(
            id=1,
            name="dummy",
            subscribers=[
                Address(
                    id=1,
                    name="John Doe",
                    email="dummy@fake.com"
                )
            ]
        )

        dcg = DeviceChunkGroup(1)
        dcg.create_device(d)
        chunks = dcg.get_chunk_group(1)

        assert len(chunks.get_chunks()) == 1

        d = Device(
            id=1,
            name="dummy",
            subscribers=[
                Address(
                    id=2,
                    name="janedoe",
                    email="janedoe@dummy.com"
                )
            ]
        )
        dcg.update_device(d)

        assert dcg.get_chunk_group(1).get_chunks()[0].subscribers == Address(
            id=2,
            name="janedoe",
            email="janedoe@dummy.com"
        )

    def test_patch_device(self):
        d = Device(
            id=1,
            name="dummy",
            subscribers=[
                Address(
                    id=1,
                    name="John Doe",
                    email="dummy@fake.com"
                )
            ]
        )

        dcg = DeviceChunkGroup(1)
        dcg.create_device(d)
        chunks = dcg.get_chunk_group(1)

        assert len(chunks.get_chunks()) == 1

        d = Device(
            id=1,
            name="dummy",
            subscribers=[
                Address(
                    id=2,
                    name="janedoe",
                    email="janedoe@dummy.com"
                )
            ]
        )
        dcg.patch_device(d)

        assert dcg.get_chunk_group(1).get_chunks()[0].subscribers == set([
            Address(
                id=1,
                name="John Doe",
                email="dummy@fake.com"
            ),
            Address(
                id=2,
                name="janedoe",
                email="janedoe@dummy.com"
            )
        ])

